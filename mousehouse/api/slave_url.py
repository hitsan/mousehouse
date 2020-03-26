import json
from flask_restful import Resource, request
from utils.logger import get_logger
from utils.connect_ip import ping_ip, arp_ip, kick_slave
from db.setting import session
from db.model.slave_table import Slave, SlaveSchema
from .url_api import *

logger = get_logger(__name__)
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
