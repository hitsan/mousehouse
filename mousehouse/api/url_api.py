import re
import json
from ipaddress import IPv4Address, AddressValueError
from flask import abort, Response
from utils.logger import get_logger
from config.config_reader import conf
from db.setting import session
from db.model.mouse_table import Mouse, MouseSchema
from sqlalchemy.orm.exc import NoResultFound

logger = get_logger(__name__)
def format_response(data, status=200):
    """
    Format json text

    Args:
        data (dictinary) : response word
        statis (int) : http status

    Returns:
        Response : Returns formatted word
    """
    response = Response(json.dumps(data, indent=int(conf["json"]["indent"])),status)
    response.headers['Content-Type'] = "application/json"
    return response

def check_ip_mac(id, ip=None, mac=None):
    """
    Check that the IP and Mac address is correct and not duplicated.

    Args:
        id (int) : ID to check
        ip (str) : IP address to check
        mac (str) : MAC address to check

    Returns:
        Mouse : Returns Moues, if there is a problem with the IP address and MAC address, execute abort_404.
    """
    if ip == None and mac == None:
        abort_404("Illegal parameter. Check your command.")
    mice = has_id(id)
    if ip is not None:
        # Check that the IP address is correct and not duplicated.
        if is_nomal_ip(ip) and (is_onlyone_ip(ip) ^ is_same_ip(id, ip)):
            mice.ip = ip
        else:
            abort_404("Illegal IP address. Check your command.")
    if mac is not None:
        # Check that the MAC address is correct and not duplicated.
        if is_nomal_mac(mac) and (is_onlyone_mac(mac) ^ is_same_mac(id, mac)):
            mice.mac = mac
        else:
            abort_404("Illegal MAC address. Check your command.")
    return mice

def has_id(id):
    """
    Check if there is a mice with the specified ID.

    Args:
        id (int) : ID to check

    Returns:
        Mouse or None : Returns if mice exists, otherwise None.
    """
    mice = session.query(Mouse).get(id)
    return None if mice is None else mice

def is_same_ip(id, ip):
    """
    Check the correspondence between ID and IP address.

    Args:
        ip (str) : IP address to check
        mac (str) : MAC address to check

    Returns:
        bool : Returns True if the ID and IP address correspond, otherwise return False
    """
    mice = session.query(Mouse).get(id)
    return True if ip == mice.ip else False

def is_same_mac(id, mac):
    """
    Check the correspondence between ID and IP address.

    Args:
        id (int) : IP address to check
        mac (str) : MAC address to check

    Returns:
        bool : Returns True if the ID and MAC address correspond, otherwise return False
    """
    mice = session.query(Mouse).get(id)
    return True if mac == mice.mac else False

def is_nomal_ip(ip):
    """
    Check if the IP address is normal.

    Args:
        ip (str) : IP address to check

    Returns:
        bool : If the specified IP address is nomaly return Ture, otherwise return False
    """
    try:
        if IPv4Address(ip) is not None:
            logger.debug("%s is normal IP address." % ip)
            return True
    except AddressValueError:
        logger.error("%s is NOT normal IP address." % ip)
        return False

def is_nomal_mac(mac):
    """
    Check if the specified MAC address is normal.

    Args:
        mac (str) : MAC address  to check

    Returns:
        bool : If the specified MAC address is nomaly return Ture, otherwise return False
    """
    mac_format = "[0-9a-f]{2}([-:])[0-9a-f]{2}(:[0-9a-f]{2}){4}$"
    return True if re.match(mac_format, mac.lower()) else False

def is_onlyone_ip(ip):
    """
    Confirm that the specified IP address is not duplicated.

    Args:
        ip (str) : IP address to check

    Returns:
        bool : Returns True if IP is duplicated, False if not.
    """
    try:
        session.query(Mouse).filter_by(ip=ip).one()
        logger.debug("%s is duplicated." % ip)
        return False
    except NoResultFound:
        logger.debug("%s is NOT duplicated." % ip)
        return True

def is_onlyone_mac(mac):
    """
    Check if the specified MAC address is duplicated.

    Args:
        mac (str) : MAC address  to check

    Returns:
        bool : If the specified MAC address is not duplicated return Ture, otherwise return False
    """
    try:
        session.query(Mouse).filter_by(mac=mac).one()
        logger.debug("%s is duplicated." % mac)
        return False
    except NoResultFound:
        logger.debug("%s is NOT duplicated." % mac)
        return True

def is_exist_id(id):
    """
    Make sure the specified ID Mice is exist.

    Args:
        id (int) : ID  to check

    Returns:
        bool : If the specified id is exist return Ture, otherwise return False
    """
    mouse = session.query(Mouse).get(id)
    return True if mouse is not None else False

def get_mice(id=None):
    """
    Fetch the mouse of the specified ID from the DB.
    If no ID is specified, get all mice.

    Args:
        id (int) : ID  to check

    Returns:
        list[Mouse] or None : Returns the mice of the specified ID, or all mices if no ID is specified.
                       If mice is not exist return None.
    """
    if id is None:
        mice = session.query(Mouse)
        return None if mice is None else MouseSchema(many=True).dump(mice)
    else:
        mice = has_id(id)
        return None if mice is None else MouseSchema().dump(mice)

def abort_404(message):
    logger.error(message)
    dic = {"message": message}
    abort(format_response(dic,404))