import os
from . import logger as lg
import configparser

class ConfigReader:
    def __init__(self):
        logger = lg.getLogger(__name__, True)
        self._conf = configparser.ConfigParser()
        try:
            home = os.environ['mousehouse_home']
            configPath =  home + '/config/config.ini'
            self._conf.read(configPath, encoding='utf-8')
        except KeyError:  
            logger.error("Please set mousehouse_home")
            exit(0)
        except TypeError:
            logger.error("Not found config.ini file. Please make config.ini file in config directory")
            exit(0)
        logger.info("Read the config.ini")

    @property
    def getConfig(self):
        return self._conf

conf = ConfigReader().getConfig