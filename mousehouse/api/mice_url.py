import json
from flask_restful import Resource, request
from utils.logger import get_logger
from utils.connect_ip import ping_ip, arp_ip, kick_mouse
from db.setting import session
from db.model.mouse_table import Mouse, MouseSchema
from .url_api import *

logger = get_logger(__name__)
class Mice(Resource):
    """
    Mice are monitored servers.
    """
    def get(self, id=None):
        """
        Show mice information in DB.
        """
        if id is None:
            mice = session.query(Mouse)
            mice_list = MouseSchema(many=True).dump(mice)
            logger.info("Get all mice information.")
        else:
            mice = has_id(id)
            mice_list = MouseSchema().dump(mice)
            logger.info("Get ID %d mice information." % id)
        dic = {
            "@url":"/mousehouse/Mice",
            "Mice" : mice_list
        }
        return format_response(dic)
         
    def post(self, id=None):
        """
        Add a monitoring server.
        Post the IP address and add server information (IP, MAC address, and status) to the DB.
        """
        logger.debug("Add mice request")
        if id is not None and session.query(Mouse).get(id) is not None:
            abort_404("This ID is exist. Cannot add the mice.")
        s_data = request.json
        try:
            ip = s_data["ip"]
            if not(is_nomal_ip(ip) and is_onlyone_ip(ip)):
                abort_404("Illegal or duplicated IP address. Check IP Address.")
            if ping_ip(ip) == 0:
                #reachable
                logger.debug("Found the mice which has %s." % ip)
                mac_addr = arp_ip(ip)
                if is_nomal_mac(mac_addr) == False:
                    mac_addr = None
                status = True
            else:
                #unreachable
                logger.debug("Not found the mice which has %s. Set MAC address and status are NULL" % ip)
                mac_addr = None
                status = False
        except KeyError:
                abort_404("POST request faile. Check your command.")
        if id is not None:
            mice = Mouse(id=id, ip=ip, mac=mac_addr, status=status)
        else:
            mice = Mouse(ip=ip, mac=mac_addr, status=status)
        session.add(mice)
        session.commit()
        logger.info("Success POST request. Add the mice in DB.")
        ret = has_id(mice.id)
        dic = {
            "@url":"/mousehouse/Mice",
            "Mice" : MouseSchema().dump(ret)
        }
        return format_response(dic, 201)

    def put(self, id=None):
        """
        Update server information(IP address and MAC address).
        """
        logger.debug("PUT request")
        if id is None:
            abort_404("No ID is designated. Designate mice ID.")
        try:
            mice = check_ip_mac(id=id, **request.json)
        except TypeError:
            abort_404("Illegal parameter. Check your command!")
        session.add(mice)
        session.commit()
        logger.info("Success PUT request. Update the mice.")
        ret = has_id(mice.id)
        dic = {
            "@url":"/mousehouse/Mice",
            "Mice" : MouseSchema().dump(ret)
        }
        return format_response(dic, 201)
    
    def delete(self, id=None):
        """
        Delete the monitoring server.
        """
        if id is None:
            abort_404("No ID is designated. Designate mice ID.")
        mice = has_id(id)
        session.delete(mice)
        session.commit()
        logger.info("Success delete ID %s mice." %id)
        return 200

class MiceAction(Resource):
    """
    Define mice action.
    """
    def get(self, id=None):
        """
        Show mice action lists.
        TODO Implement the script execution function.
        """
        mice = has_id(id)
        action_list = {"power": ["on"]}
        logger.info("Get action list." )
        dic = {
            "@url":"/mousehouse/Mice/%s/Action" % id,
            "Action" : action_list
        }
        return format_response(dic)

class MicePower(Resource):
    """
    Define mice Power action.
    """
    def post(self, id=None):
        """
        Control mice power
        TODO Implement reset and shutdown.
        """
        data = request.json
        mice = has_id(id)
        try:
            if data["power"] == "on":
                if ping_ip(mice.ip) == 0:
                    abort_404("ID %s is alreadt booted.")
                if mice.mac == None:
                    abort_404("MAC address is not define.")
                kick_mouse(mice.mac)  
        except KeyError:
            abort_404("Illegal Power parameter.")
        return 202
