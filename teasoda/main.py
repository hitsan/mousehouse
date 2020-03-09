#!/usr/bin/env python
import time
import os
import sys
import configparser

#logger

#read and set config
def readConfig():
    config = configparser.ConfigParser()
    config_ini_path = '../config/config.ini'
    if config_ini_path is None:
        print("Not found config.ini file")
        print("Please make config.ini file in config directory")
        exit(0)
    config.read(config_ini_path, encoding='utf-8')

#deamonize
#def daemonize():
#    pid = os.fork()
#    if pid > 0:


if __name__=='__main__':
    readConfig()