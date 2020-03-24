import subprocess
import socket
import binascii
from utils import logger as lg

logger = lg.getLogger(__name__)
def pingIP(ip):
    """
    Check the IP address is reachable.
    """
    com = 'ping -c1 -w1 ' + ip
    return subprocess.call(com.split(),stdout = subprocess.DEVNULL,stderr = subprocess.DEVNULL)

def arpIP(ip):
    """
    Return MAC Address from IP
    """
    com = 'arp -a ' + ip
    try:
        line = subprocess.check_output(com.split())
        return str(line).split(' ')[3]
    except IndexError:
        logger.error("Can not get MAC address.")
        return None

def kickSlave(mac):
    """
    Power on slave by sending magic packet
    """
    broadcast = '255.255.255.255'
    port = 7

    macadd = ''.join(mac.split(':'))
    mdata = 'FF' * 6 + macadd * 16
    mdata = binascii.unhexlify(mdata)

    con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    con.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    con.sendto(mdata, (broadcast, port))
    logger.info("Send magic packet to %s" % mac)
 
    con.close()
