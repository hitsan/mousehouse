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
    BROAD_CAST = '255.255.255.255'
    PORT = 7

    m_data = 'FF' * 6 + ''.join(mac.split(':')) * 16
    magic_packet = binascii.unhexlify(m_data)

    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    connection.sendto(magic_packet, (BROAD_CAST, PORT))
    logger.info("Send magic packet to %s" % mac)
    connection.close()
