#!/usr/bin/env python
import time
import sys
import errno
import logging
import os
import time
from utils.configReader import conf
from utils import logger as lg
from rest.restMain import app
from db.dbManager import engine, Base

def initialize():
    """
    Initialzation mousehouse.
    Start logging and daemonization
    """
    logger = lg.getLogger(__name__, True)
    logger.info('Initialize mousehouse')

    Base.metadata.create_all(bind=engine)
    #print(conf['logging']['logFlie'])
   

if __name__=='__main__':
    #initialize()
    """
    machien = Machine(ip_addr="192.168.11.2", mac_addr="mac")
    session.add(machien)
    session.commit()
    """

    #app.run(debug=True)

    #Daemonaze
    """
    pid = os.fork()
    if pid > 0:
        pid_file = open('./mousehouse.pid','w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
        
    if pid == 0:
        _initialize()
    """