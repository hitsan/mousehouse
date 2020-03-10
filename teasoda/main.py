#!/usr/bin/env python
import time
import os
import sys
import configparser
from flask import Flask
from rest import manager, machines

app = Flask(__name__)
app.register_blueprint(manager.app, url_prefix = '/teadoda/v1')
#app.register_blueprint(machines, url_prefix = '/teadoda/v1')

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
    app.run(bebug = True, host = '127.0.0.1')