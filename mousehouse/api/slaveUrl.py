import re
import json
from ipaddress import IPv4Address, AddressValueError
from collections import OrderedDict
from flask import Blueprint, jsonify, make_response, abort, Response
from flask_restful import Resource, request
from utils.logger import getLogger
from utils.configReader import conf
from utils.connectIP import ping_ip, arp_ip, kick_slave
from db.dbSetting import session
from db.model.slaveTable import Slave, SlaveSchema
from sqlalchemy.orm.exc import NoResultFound

logger = getLogger(__name__)
class Slaves(Resource):
    """
    Slaves are monitored servers.
    """
    def get(self, id=None):
        """
        Show slaves information in DB.
        """
        if id is None:
            slaves = session.query(Slave)
            slave_list = SlaveSchema(many=True).dump(slaves)
            logger.info("Get all slaves information.")
        else:
            slave = has_id(id)
            slave_list = SlaveSchema().dump(slave)
            logger.info("Get ID %d slave information." % id)
        dic = {
            "@url":"/mousehouse/slaves",
            "slaves" : slave_list
        }
        return format_response(dic)
         
    def post(self, id=None):
        """
        Add a monitoring server.
        Post the IP address and add server information (IP, MAC address, and status) to the DB.
        """
        logger.info("Add slave request")
        if id is not None and session.query(Slave).get(id) is not None:
            abort_404("This ID is exist. Cannot add the slave.")
        s_data = request.json
        try:
            ip = s_data["ip"]
            if not(is_nomal_ip(ip) and is_onlyone_ip(ip)):
                abort_404("Illegal IP address. Check IP Address.")
            if ping_ip(ip) == 0:
                #reachable
                logger.info("Found the slave which has %s." % ip)
                mac_addr = arp_ip(ip)
                if is_nomal_mac(mac_addr) == False:
                    mac_addr = None
                status = True
            else:
                #unreachable
                logger.info("Not found the slave which has %s. Set MAC address and status are NULL" % ip)
                mac_addr = None
                status = False
        except KeyError:
                abort_404("POST request faile. Check your command.")
        if id is not None:
            slave = Slave(id=id, ip=ip, mac=mac_addr, status=status)
        else:
            slave = Slave(ip=ip, mac=mac_addr, status=status)
        session.add(slave)
        session.commit()
        logger.info("Success POST request. Add the slave in DB.")
        ret = has_id(slave.id)
        dic = {
            "@url":"/mousehouse/slaves",
            "slaves" : SlaveSchema().dump(ret)
        }
        return format_response(dic, 201)

    def put(self, id=None):
        """
        Update server information(IP address and MAC address).
        """
        logger.info("PUT request")
        if id is None:
            abort_404("No ID is designated. Designate slave ID.")
        try:
            slave = check_ip_mac(id=id, **request.json)
        except TypeError:
            abort_404("Illegal parameter. Check your command!")
        session.add(slave)
        session.commit()
        logger.info("Success PUT request. Update the slave.")
        ret = has_id(slave.id)
        dic = {
            "@url":"/mousehouse/slaves",
            "slaves" : SlaveSchema().dump(ret)
        }
        return format_response(dic, 201)
    
    def delete(self, id=None):
        """
        Delete the monitoring server.
        """
        if id is None:
            abort_404("No ID is designated. Designate slave ID.")
        slave = has_id(id)
        session.delete(slave)
        session.commit()
        return 200

class SlaveAction(Resource):
    """
    Define Slave action.
    """
    def get(self, id=None):
        """
        Show slave action lists.
        TODO Implement the script execution function.
        """
        slave = has_id(id)
        action_list = {"power": ["on"]}
        logger.info("Get action list." )
        dic = {
            "@url":"/mousehouse/Slaves/%s/Action" % id,
            "Action" : action_list
        }
        return format_response(dic)

class SlavePower(Resource):
    """
    Define Slave Power action.
    """
    def post(self, id=None):
        """
        Control slave power
        TODO Implement reset and shutdown.
        """
        data = request.json
        slave = has_id(id)
        try:
            if data["power"] == "on":
                if ping_ip(slave.ip) == 0:
                    abort_404("ID %s is alreadt booted.")
                if slave.mac == None:
                    abort_404("MAC address is not define.")
                kick_slave(slave.mac)  
        except KeyError:
            abort_404("Illegal Power parameter.")
        return 202

def format_response(data, status=200):
    """
    Format json text
    """
    response = Response(json.dumps(data, indent=int(conf["json"]["indent"])),status)
    response.headers['Content-Type'] = "application/json"
    return response

def check_ip_mac(id, ip=None, mac=None):
    """
    Check IP and MAC address.
    If there is no problem, return the slave.
    """
    if ip == None and mac == None:
        abort_404("Illegal parameter. Check your command.")
    slave = has_id(id)
    if ip is not None:
        if is_nomal_ip(ip) and (is_onlyone_ip(ip) ^ is_same_ip(id, ip)):
            slave.ip = ip
        else:
            abort_404("Illegal IP address. Check your command.")
    if mac is not None:
        if is_nomal_mac(mac) and (is_onlyone_mac(mac) ^ is_same_mac(id, mac)):
            slave.mac = mac
        else:
            abort_404("Illegal MAC address. Check your command.")
    return slave

def has_id(id):
    """
    Check if there is a slave with the specified ID.
    Returns if slave exists, otherwise respond 404.
    """
    slave = session.query(Slave).get(id)
    if slave is None:
        abort_404("Not found ID %d slave." % id)
    return slave

def is_same_ip(id, ip):
    """
    Check the correspondence between ID and IP address
    """
    slave = session.query(Slave).get(id)
    logger.info("IP address is %s" % slave.ip)
    return True if ip == slave.ip else False

def is_same_mac(id, mac):
    """
    Check the correspondence between ID and IP address
    """
    slave = session.query(Slave).get(id)
    return True if mac == slave.mac else False

def is_nomal_ip(ip):
    """
    Check if the IP address is normal.
    """
    try:
        if IPv4Address(ip) is not None:
            logger.info("%s is normal IP address." % ip)
            return True
    except AddressValueError:
        logger.error("%s is NOT normal IP address." % ip)
        return False

def is_nomal_mac(mac):
    """
    Check if the MAC address is normal.
    """
    mac_format = "[0-9a-f]{2}([-:])[0-9a-f]{2}(:[0-9a-f]{2}){4}$"
    return True if re.match(mac_format, mac.lower()) else False

def is_onlyone_ip(ip):
    """
    Check if the IP address is duplicated.
    """
    try:
        session.query(Slave).filter_by(ip=ip).one()
        logger.info("%s is duplicated." % ip)
        return False
    except NoResultFound:
        logger.info("%s is NOT duplicated." % ip)
        return True

def is_onlyone_mac(mac):
    """
    Check if the MAC address is duplicated.
    """
    try:
        session.query(Slave).filter_by(mac=mac).one()
        logger.info("%s is duplicated." % mac)
        return False
    except NoResultFound:
        logger.info("%s is NOT duplicated." % mac)
        return True

def abort_404(message):
    logger.error(message)
    dic = {"message": message}
    abort(format_response(dic,404))