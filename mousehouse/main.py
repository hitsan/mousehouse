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
    Base.metadata.create_all(bind=engine)   

if __name__=='__main__':
    initialize()
    monitor_thread = MiceMonitor()
    monitor_thread.start()
    app.run(
        debug=True,
        host=conf["master"]["ip"],
        port= conf["master"]["port"]
        )
