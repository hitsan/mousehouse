import re
from ipaddress import *
import subprocess as sbp
from flask import Blueprint, jsonify, make_response, abort
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
        If DB is empty, return empty list.
        """
        if id is None:
            slaves = session.query(Slave)
            ret = SlaveSchema(many=True).dump(slaves)
            logger.info("Get all slaves information.")
        elif id > 0:
            slave = session.query(Slave).get(id)
            ret = SlaveSchema().dump(slave)
            logger.info("Get ID %d slave information." % id)
        
        return make_response(jsonify({
            "@odata.id":"/mousehouse/slaves",
            "slaves" : ret
        }))
         
    def post(self):
        """
        Add a monitoring server.
        Post the IP address and add server information (IP, MAC address, and status) to the DB.
        """
        logger.info("POST request")
        s_data = request.json
        try:
            ip = s_data["ip"]
            ping = 'ping -c1 ' + str(ip)
            arp = 'arp -a ' + str(ip)
            if _isNomalIP(ip) and _isOnlyOneIP(ip):
                if sbp.call(ping.split(),stdout = sbp.DEVNULL,stderr = sbp.DEVNULL) == 0:
                    line = sbp.check_output(arp.split())
                    macaddr = str(line).split(' ')[3]
                    status = True
                else:
                    macaddr = None
                    status = False
        except KeyError:
                logger.error("POST request faile. Check your command.")
                abort(404)

        slave = Slave(ip=ip, mac=macaddr, status=status)
        session.add(slave)
        session.commit()
        logger.info("POST request success. Add slave in DB.")
        return 200

def _isNomalIP(ip):
    """
    Check if the IP address is normal.
    """
    try:
        if IPv4Address(ip) is not None:
            logger.info("%s is normal IP address." % str(ip))
            return True
    except AddressValueError:
        logger.error("%s is NOT normal IP address." % str(ip))
        return False

def _isOnlyOneIP(ip):
    """
    Check if the IP address is duplicated.
    """
    try:
        session.query(Slave).filter_by(ip=ip).one()
        logger.info("%s is duplicated." % str(ip))
        return False
    except NoResultFound:
        logger.info("%s is NOT duplicated." % str(ip))
        return True