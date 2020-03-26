import subprocess
import socket
import binascii
from utils.logger import get_logger

logger = get_logger(__name__)
def ping_ip(ip):
    """
    Check the IP address is reachable.
    """
    com = 'ping -c1 -w1 ' + ip
    return subprocess.call(com.split(),stdout = subprocess.DEVNULL,stderr = subprocess.DEVNULL)

def arp_ip(ip):
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

def kick_slave(mac):
    """
    Power on slave by sending magic packet
    """
    broadcast = '255.255.255.255'
    port = 7

    mac_add = ''.join(mac.split(':'))
    m_data = 'FF' * 6 + mac_add * 16
    m_data = binascii.unhexlify(m_data)

    con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    con.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    con.sendto(m_data, (broadcast, port))
    logger.info("Send magic packet to %s" % mac)
 
    con.close()
