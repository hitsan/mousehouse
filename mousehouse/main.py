#!/usr/bin/env python
import time
import sys
import errno
import logging
import os
import time
from utils.configReader import conf
from utils.logger import getLogger
from api.restMain import app
from db.dbSetting import engine, Base

def initialize():
    """
    Initialzation mousehouse.
    Start logging and setup DB.
    """
    logger = getLogger(__name__, True)
    logger.info('Initialize mousehouse')

    Base.metadata.create_all(bind=engine)   

if __name__=='__main__':
    initialize()
    #app.run(debug=True, host=conf["master"]["ip"], port= conf["master"]["port"])
    app.run(host=conf["master"]["ip"], port= conf["master"]["port"])
    #Daemonaze
    """
    path = os.path.abspath(__file__)
    pid_path = path[:-18] + '.mousehouse.pid'
    print(pid_path)
    pid = os.fork()
    if pid > 0:
        pid_file = open(pid_path,'w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
        
    if pid == 0:
            app.run(host=conf["master"]["ip"], port= conf["master"]["port"])
    """