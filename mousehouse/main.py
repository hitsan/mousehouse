#!/usr/bin/env python
import time
import sys
import errno
import logging
import os
import time
from utils.configReader import ConfigReader as cr
from utils import logger as lg

#Initialzation mousehouse.
#Start logging and daemonization
def _initialize():
    #Start logging
    logger = lg.getLogger(__name__, 'logs/master.log')
    logger.info('Init mousehouse')
    

if __name__=='__main__':
    #Daemonaze
    pid = os.fork()
    if pid > 0:
        pid_file = open('./mousehouse.pid','w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
        
    if pid == 0:
        _initialize()