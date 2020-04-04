import time
import sys
import errno
import logging
import os
import threading
from config.config_reader import conf
from utils.logger import get_logger
from api.rest import app
from db.setting import engine, Base
from monitor import MiceMonitor

from api.authentication import add_users

logger = get_logger(__name__, True)
def initialize():
    """
    Initialzation mousehouse.
    Start logging and setup DB.
    """
    logger.info('Initialize mousehouse')
    time_out = 5
    while time_out > 0:
        try:
            Base.metadata.create_all(bind=engine)
        except:
            time_out -= 1
            time.sleep(1)
            if time_out == 0:
                logger.error("Cannot connect DB server. Check config.ini file.")
                exit(0)
        else:
            time_out = -1

if __name__=='__main__':
    initialize()
    monitor_thread = MiceMonitor()
    monitor_thread.start()
    app.run(
        debug=True,
        host=conf["master"]["ip"],
        port= conf["master"]["port"]
        )
