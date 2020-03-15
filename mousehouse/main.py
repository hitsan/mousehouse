#!/usr/bin/env python
import time
import sys
import errno
import logging
from utils.configReader import ConfigReader as cr

#logger
def startLogging(logfile_path):
    logging.basicConfig(filename=logfile_path,level=logging.DEBUG)

def initialize():
    #Read config file
    conf = cr.getConfig()
    logfile_path = conf['logging']['logfile_path']
    print(logfile_path)

#deamonize
#def daemonize():
#    pid = os.fork()
#    if pid > 0:

if __name__=='__main__':
    initialize()