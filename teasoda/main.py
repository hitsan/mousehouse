#!/usr/bin/env python
import time
import os
import sys
import configparser
import errno
import logging

home = os.environ['Teasoda_home']

#logger
def startLogging(logfile_path):
    logging.basicConfig(filename=logfile_path,level=logging.DEBUG)

def initialize():
    #read config file
    config = configparser.ConfigParser()
    config_ini_path =  home + '/config/config.in'
    if not os.path.exists(config_ini_path):
        print("Not found config.ini file. Please make config.ini file in config directory")
        exit(0)
    config.read(config_ini_path, encoding='utf-8')
    logfile_path = config['logging']['logfile_path']
    startLogging(logfile_path)


#deamonize
#def daemonize():
#    pid = os.fork()
#    if pid > 0:


if __name__=='__main__':
    initialize()