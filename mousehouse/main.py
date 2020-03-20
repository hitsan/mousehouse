#!/usr/bin/env python
import time
import sys
import errno
import logging
import os
import time
from utils import configReader as cr
from utils import logger as lg
from db import dbManager as dbm
from rest.restMain import app

def initialize():
    """
    Initialzation mousehouse.
    Start logging and daemonization
    """
    logger = lg.getLogger(__name__, True)
    logger.info('Initialize mousehouse')
    #print(cr.conf['logging']['logFlie'])
   

if __name__=='__main__':
    initialize()
    #dbm.dbSetup()
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