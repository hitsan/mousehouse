import re
import json
from ipaddress import IPv4Address, AddressValueError
from flask import abort, Response
from utils.logger import get_logger
from utils.config_reader import conf
from db.setting import session
from db.model.slave_table import Slave
from sqlalchemy.orm.exc import NoResultFound

logger = get_logger(__name__)
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