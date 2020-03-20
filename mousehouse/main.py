#!/usr/bin/env python
import time
import sys
import errno
import logging
import os
import time
from utils.configReader import ConfigReader as cr
from utils import logger as lg
from db import dbManager as dbm
from rest.restMain import app

def _initialize():
    """
    Initialzation mousehouse.
    Start logging and daemonization
    """
    logger = lg.getLogger(__name__, True)
    logger.info('Initialize mousehouse')
    #conf = cr.getConfig()
    

if __name__=='__main__':
    dbm.dbSetup()
    app.run(debug=True)

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