import time
import json
import threading
from config.config_reader import conf
from utils.logger import get_logger
from utils.connect_ip import ping_ip
from db.setting import session
from db.model.mouse_table import Mouse, MouseSchema

logger = get_logger(__name__)
class MiceMonitor(threading.Thread):
    """
    Monitoring Mice
    """
    def __init__(self):
        threading.Thread.__init__(self)

    def __monitor(self):
        """
        Monitoring mice.
        Determine whether connection is possible.
        """
        all_mice = session.query(Mouse.id, Mouse.ip).all()
        if all_mice is None:
            return
        ip_dic = MouseSchema(many=True).dump(all_mice)
        id_status = self.__alive_mouse(ip_dic)
        self.__update_status(id_status)

    def __alive_mouse(self, ip_dic):
        """
        Make sure the mouse is alive or not.
        Return 
        """
        status ={}
        for mouse in ip_dic:
            status[mouse['id']] = True if  ping_ip(mouse['ip']) == 0 else False
        return json.dumps(status)
    
    def __update_status(self, id_status):
        """
        Updata mice status
        commit 
        """
        id_status = json.loads(id_status)
        for dic in id_status:
            mouse = session.query(Mouse).filter(Mouse.id==dic).first()
            mouse.status = id_status[dic]
        session.commit()

    def run(self):
        """
        Call monitor at regular intervals
        """
        try:
            interval = int(conf['monitoring']['interval'])
        except KeyError:
            logger.error("The interval time is invalid. Set to 30 sec.")
            interval=30
        logger.info("Monitoring interval time is %s sec" % interval)
        while True:
            self.__monitor()
            time.sleep(interval)
    