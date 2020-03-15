#!/usr/bin/env python
import time
import sys
import errno
import logging
#import subprocess
from utils.configReader import ConfigReader as cr

#logger
def _startLogging():
    #conf = cr.getConfig()
    #log_dir = conf['logging']['log_dir']
    #log = subprocess.check_output(['echo', log_dir])
    #print(log)
    logging.basicConfig(filename=logs/master.log,level=logging.DEBUG)

def initialize():
    #Read config file
    #conf = cr.getConfig()
    #logfile_path = conf['logging']['logfile_path']
    #print(logfile_path)
    _startLogging()

#deamonize
#def daemonize():
#    pid = os.fork()
#    if pid > 0:

if __name__=='__main__':
    initialize()