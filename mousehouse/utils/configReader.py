import configparser
import os
from utils import logger as lg

class ConfigReader:
    _config_reader = None
    _conf = None
    def __new__(cls):
        if cls._configReader is None:
            cls._configReader = super().__new__(cls)
        return cls._configReader

    @classmethod
    def getConfig(cls):
        #return cls._config_reader
        logger = lg.getLogger(__name__, True)
        if cls._conf is None:
            logger.info("Start reading the config.ini")
            cls._conf = configparser.ConfigParser()
            try:
                home = os.environ['mousehouse_home']
                configPath =  home + '/config/config.ini'
                cls._conf.read(configPath, encoding='utf-8')
            except KeyError as e:  
                logger.error("Please set mousehouse_home")
                exit(0)
            except TypeError:
                logger.error("Not found config.ini file. Please make config.ini file in config directory")
                exit(0)
        return cls._conf
