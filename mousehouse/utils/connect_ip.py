import subprocess
import socket
import binascii
from api.url_api import is_nomal_mac
from utils.logger import get_logger

logger = get_logger(__name__)
def ping_ip(ip):
    """
    Check the IP address is reachable.

    Args:
        ip (str) : IP address to check

    Returns:
        bool : Returns True if the IP address is reachable, False otherwise.
    """
    com = 'ping -c1 -w1 ' + ip
    reach_status = subprocess.call(com.split(),stdout = subprocess.DEVNULL,stderr = subprocess.DEVNULL)
    return True if reach_status == 0 else False

def arp_ip(ip):
    """
    Return MAC Address from IP

    Args:
        ip (str) : Ip with the mac you want to know.

    Returns:
        str or None : Returns True if the IP address is reachable, False otherwise.
    """
    com = 'arp -a ' + ip
    try:
        line = subprocess.check_output(com.split())
        mac = [x for  x in str(line).split(' ') if is_nomal_mac(x)][0]
        if mac is None:
            logger.error("Can not get MAC address.")
            return None
        return mac
    except IndexError:
        logger.error("Can not get MAC address.")
        return None

def kick_mouse(mac):
    """
    Power on mouse by sending magic packet

    Args:
        mac (str) : Ip with the mac you want to know.
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
