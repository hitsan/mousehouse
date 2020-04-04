import json
from flask_restful import Resource, request
from utils.logger import get_logger
from utils.connect_ip import ping_ip, arp_ip, kick_mouse
from db.setting import session
from db.model.mouse_table import Mouse, MouseSchema
from .url_api import *
from werkzeug.security import generate_password_hash
from .authentication import authenticate

logger = get_logger(__name__)
class Mice(Resource):
    """
    Mice are monitored servers.
    """
    @authenticate
    def get(self):
        """
        Show mice information in DB.

        Returns:
            Response : Mice list
        """
        mice_list = get_mice(None)
        if not mice_list:
            abort_400("Mice is nothing!")
        dic = {
            "@url":"/mousehouse/Mice",
            "Mice" : mice_list
        }
        return format_response(dic)
    
    @authenticate
    def post(self):
        """
        Add a monitoring server.
        Following the POST parameters.
        ["ID", "IP", "MAC", "Status", "OS", "User", "Password", "Description"]
        At least the IP address must be specified in the POST request.

        Returns:
            Response : Added Mice
        """
        logger.debug("POST request")
        
        # Check Invaild parameters.
        post_data = request.json
        correct_request_parameter(post_data)

        # Check the parameters.
        # IP address check.
        if "IP" in post_data.keys():
            ip = post_data["IP"]
            logger.debug("Set IP address %s " % ip)
            if not(is_nomal_ip(ip) and is_onlyone_ip(ip)):
                abort_400("Invaild or duplicated IP address. Check IP Address.", 403)
        else:
            abort_400("IP address is nothing! Set IP address.", 403)
        
        # ID Check.
        if "ID" in post_data.keys():
            id = post_data["ID"]
            logger.debug("Set ID %s " % id)
            if is_exist_id(id):
                abort_400("ID %s is duplicated. Change ID number." % id ,403)
        else:
            id = None
    
        # Status check
        if ping_ip(ip) == True:
            status = True
        else:
            status = False
        logger.debug("Set Status %s " % status)

        # MAC address check
        if "MAC" in post_data.keys():
            mac = post_data["MAC"]
            logger.debug("Set MAC addres %s " % mac)
            if not(is_nomal_mac(mac) and (is_onlyone_mac(mac))):
                abort_400("Invaild or duplicated MAC address. Check MAC Address.", 403)
        else:
            mac ="auto"
        
        # MAC address search.
        if mac == "auto" and status == True:
            mac = arp_ip(ip)
            logger.debug("Set MAC addres %s automatic" % mac)
        else:
            mac =None
        if is_nomal_mac(mac) == False:
            mac = None
        
        # User and Password check.
        # User and Password are set at the same time in POST request.
        if ("User" in post_data.keys()) ^ ("Password" in post_data.keys()):
            abort_400("Set the User and Password at the same time." , 403)
        elif "User" in post_data.keys():
            user = post_data["User"]
            password = post_data["Password"]
            # Hash Password
            password = generate_password_hash(password)
            logger.debug("Set User and Password")
        else:
            user = None
            password = None

        # OS check
        # There is a possibility to implement OS discrimination function in the future.
        if "OS" in post_data.keys():
            os = post_data["OS"]
            logger.debug("Set OS")
        else:
            os = None

        # Host name check
        if "Host" in post_data.keys():
            host = post_data["Host"]
            logger.debug("Set Host name.")
        else:
            host = None

        # Description check
        if "Description" in post_data.keys():
            description = post_data["Description"]
            logger.debug("Set Description.")
        else:
            description = None

        # Commit mice
        if id is None:
            mice = Mouse(IP=ip, MAC=mac, Status=status, OS=os, User=user, Password=password, Host=host, Description=description)
        else:
            mice = Mouse(ID=id, IP=ip, MAC=mac, Status=status, OS=os, User=user, Password=password, Host=host, Description=description)
        session.add(mice)
        session.commit()
        logger.info("Success POST request. Add the mice in DB.")
        ret = has_id(mice.ID)
        dic = {
            "@url":"/mousehouse/Mice",
            "Mice" : MouseSchema().dump(ret)
        }
        return format_response(dic, 201)

class MiceID(Resource):
    """
    Mice are monitored servers.
    """
    @authenticate
    def get(self, id):
        """
        Show mice information in DB.

        Args:
            id (int) or None : Mice to get

        Returns:
            Response : Mice list
        """
        mice_list = get_mice(id)
        if mice_list is None:
            abort_400("ID %s Mice is nothing" % id)
        dic = {
            "@url":"/mousehouse/Mice",
            "Mice" : mice_list
        }
        return format_response(dic)

    @authenticate
    def put(self, id):
        """
        Update server information(IP address and MAC address).

        Args:
            id (int) : ID specified when puting

        Returns:
            Response : Modified Mice
        """
        logger.debug("PUT request")

        mice = has_id(id)
        if mice is None:
            abort_400("ID %s Mice is nothing" % id)
        
        # Check Invaild parameters.
        post_data = request.json
        correct_request_parameter(post_data)

        # Check the parameters.

        # ID Check.
        if "ID" in post_data.keys() and post_data["ID"] != mice.ID:
            abort_400("ID cannot be rewritten." ,403)

        # IP address check.
        if "IP" in post_data.keys():
            ip = post_data["IP"]
            mice.IP = ip
            logger.debug("Set IP address %s " % ip)
            if not( is_nomal_ip(ip) and (is_onlyone_ip(ip) ^ is_same_ip(id, ip)) ):
                abort_400("Invaild or duplicated IP address. Check IP Address.", 403)

        # MAC address check
        # 
        if "MAC" in post_data.keys():
            mac = post_data["MAC"]
            mice.MAC = mac
            logger.debug("Set MAC")
            if not( is_nomal_mac(mac) and (is_onlyone_mac(mac) ^ is_same_mac(id, mac)) ):
                abort_400("Invaild or duplicated MAC address. Check MAC Address.", 403)
    
        # User check
        # 
        if "User" in post_data.keys():
            user = post_data["User"]
            mice.User = user
            logger.debug("Set User")

        # Password check
        # 
        if "Password" in post_data.keys():
            password = post_data["Password"]
            mice.Password = generate_password_hash(password)
            logger.debug("Set Password")

        # OS check
        # There is a possibility to implement OS discrimination function in the future.
        if "OS" in post_data.keys():
            os = post_data["OS"]
            mice.OS = os
            logger.debug("Set OS")

        # Host name check
        if "Host" in post_data.keys():
            host = post_data["Host"]
            mice.Host = host
            logger.debug("Set Host name.")

        # Description check
        if "Description" in post_data.keys():
            description = post_data["Description"]
            mice.Description = description
            logger.debug("Set Description.")

        # Commit mice    
        session.add(mice)
        session.commit()
        logger.info("Success PUT request. Update the mice.")
        ret = has_id(mice.ID)
        dic = {
            "@url":"/mousehouse/Mice",
            "Mice" : MouseSchema().dump(ret)
        }
        return format_response(dic, 201)

    @authenticate
    def delete(self, id):
        """
        Delete the monitoring server.

        Args:
            id (int) : ID specified when deleting

        Returns:
            Response : http status 200
        """
        mice = has_id(id)
        if mice is None:
            abort_400("Cannot delete ID %s Mice is nothing" % id)
        session.delete(mice)
        session.commit()
        logger.info("Success delete ID %s mice." %id)
        return 200

class MiceAction(Resource):
    """
    Define mice action.
    """
    @authenticate
    def get(self, id):
        """
        Show mice action lists.
        TODO Implement the script execution function.

        Args:
            id (int) : ID specified when puting the action

        Returns:
            Response : Action list
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
    @authenticate
    def post(self, id=None):
        """
        Control mice power
        TODO Implement reset and shutdown.

        Args:
            id (int) : ID specified when power on

        Returns:
            Response : http status 202
        """
        data = request.json
        mice = has_id(id)
        try:
            if data["power"] == "on":
                if ping_ip(mice.ip) == True:
                    abort_400("ID %s is alreadt booted.")
                if mice.mac == None:
                    abort_400("MAC address is not define.")
                kick_mouse(mice.mac)  
        except KeyError:
            abort_400("Invaild Power parameter.")
        return 202
