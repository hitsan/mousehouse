#!/usr/bin/env python
import time
import sys
import errno
import logging
import os
import time
from utils.configReader import conf
from utils import logger as lg
from api.restMain import app
from db.dbSetting import engine, Base

def initialize():
    """
    Initialzation mousehouse.
    Start logging and setup DB.
    """
    logger = lg.getLogger(__name__, True)
    logger.info('Initialize mousehouse')

    Base.metadata.create_all(bind=engine)   

if __name__=='__main__':
    initialize()
    #app.run(debug=True, host=int(conf["master"]["ip"]), port=int(conf["master"]["ip"]))
    app.run(debug=True, \
        host=conf["master"]["ip"],\
        port= conf["master"]["port"])
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