import re
import json
from ipaddress import *
import subprocess as sbp
from flask import Blueprint, jsonify, make_response, abort, Response
from flask_restful import Resource, request
from utils import logger as lg
from db.dbSetting import session
from db.model.slaveTable import Slave, SlaveSchema
from sqlalchemy.orm.exc import NoResultFound

logger = lg.getLogger(__name__)
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
            ret = SlaveSchema(many=True).dump(slaves)
            logger.info("Get all slaves information.")
        else:
            slave = _hasId(id)
            ret = SlaveSchema().dump(slave)
            logger.info("Get ID %d slave information." % id)
        
        return make_response(jsonify({
            "@odata.id":"/mousehouse/slaves",
            "slaves" : ret
        }))
         
    def post(self, id=None):
        """
        Add a monitoring server.
        Post the IP address and add server information (IP, MAC address, and status) to the DB.
        """
        logger.info("POST request")
        if id is not None and session.query(Slave).get(id) is not None:
            _abort404("This ID is exist. Change ID.")
        s_data = request.json
        try:
            ip = s_data["ip"]
            ping = 'ping -c1 ' + ip
            arp = 'arp -a ' + ip
            if not(_isNomalIP(ip) and _isOnlyOneIP(ip)):
                _abort404("Illegal IP address. Check IP Address.")
            if sbp.call(ping.split(),stdout = sbp.DEVNULL,stderr = sbp.DEVNULL) == 0:
                logger.info("Found the slave which has %s." % ip)
                line = sbp.check_output(arp.split())
                macaddr = str(line).split(' ')[3]
                status = True
            else:
                logger.info("Not found the slave which has %s. Set MAC address and status are NULL" % ip)
                macaddr = None
                status = False
        except KeyError:
                _abort404("POST request faile. Check your command.")
        if id is not None:
            slave = Slave(id=id, ip=ip, mac=macaddr, status=status)
        else:
            slave = Slave(ip=ip, mac=macaddr, status=status)
        session.add(slave)
        session.commit()
        logger.info("Success POST request. Add the slave in DB.")
        ret = _hasId(slave.id)
        return make_response(jsonify({
            "@odata.id":"/mousehouse/slaves",
            "slaves" : SlaveSchema().dump(ret)
        }))

    def put(self, id=None):
        """
        Update server information(IP address and MAC address).
        """
        logger.info("PUT request")
        if id is None:
            _abort404("No ID is designated. Designate slave ID.")
        try:
            slave = _checkIPandMac(id=id, **request.json)
        except TypeError:
            _abort404("Illegal parameter. Check your command!")
        session.add(slave)
        session.commit()
        logger.info("Success PUT request. Update the slave.")
        ret = _hasId(slave.id)
        return make_response(jsonify({
            "@odata.id":"/mousehouse/slaves",
            "slaves" : SlaveSchema().dump(ret)
        }))
    
    def delete(self, id=None):
        """
        Delete the monitoring server.
        """
        if id is None:
            _abort404("No ID is designated. Designate slave ID.")
        slave = _hasId(id)
        session.delete(slave)
        session.commit()
        return 200

def _checkIPandMac(id, ip=None, mac=None):
    """
    Check IP and MAC address.
    If there is no problem, return the slave.
    """
    if ip == None and mac == None:
        _abort404("Illegal parameter. Check your command.")
    slave = _hasId(id)
    if ip is not None:
        if _isNomalIP(ip) and (_isOnlyOneIP(ip) ^ _isSameIP(id, ip)):
            slave.ip = ip
        else:
            _abort404("Illegal IP address. Check your command.")
    if mac is not None:
        if _isNomalMac(mac) and (_isOnlyOneMac(mac) ^ _isSameMac(id, mac)):
            slave.mac = mac
        else:
            _abort404("Illegal MAC address. Check your command.")
    return slave

def _hasId(id):
    """
    Check if there is a slave with the specified ID.
    Returns if slave exists, otherwise respond 404.
    """
    slave = session.query(Slave).get(id)
    if slave is None:
        _abort404("Not found ID %d slave." % id)
    return slave

def _isSameIP(id, ip):
    """
    Check the correspondence between ID and IP address
    """
    slave = session.query(Slave).get(id)
    logger.info("IP address is %s" % slave.ip)
    return True if ip == slave.ip else False

def _isSameMac(id, mac):
    """
    Check the correspondence between ID and IP address
    """
    slave = session.query(Slave).get(id)
    return True if mac == slave.mac else False

def _isNomalIP(ip):
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

def _isNomalMac(mac):
    """
    Check if the MAC address is normal.
    """
    mac_format = "[0-9a-f]{2}([-:])[0-9a-f]{2}(:[0-9a-f]{2}){4}$"
    return True if re.match(mac_format, mac.lower()) else False

def _isOnlyOneIP(ip):
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

def _isOnlyOneMac(mac):
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

def _abort404(word):
    logger.error(word)
    abort(404, word)