"""
import logging
import os

class MouseHouseLog:
    _conf = None
    logging.basicConfig(level=logging.INFO)
    def __new__(cls):
        if cls._configReader is None:
            cls._configReader = super().__new__(cls)
        return cls._configReader

    def getLogger(self):
        logger = logging.getLogger(self)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('my-format')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger


    @classmethod
    def _initLogging(cls):
        #create logger
        log
        if os.path.isfile()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    @classmethod
    def getConfig(cls):
        #return cls._config_reader
        if cls._conf is None:
            cls._conf = configparser.ConfigParser()
            try:
                home = os.environ['mousehouse_home']
                configPath =  home + '/config/config.ini'
                cls._conf.read(configPath, encoding='utf-8')
            except KeyError as e:  
                print("Please set mousehouse_home")
                exit(0)
            except TypeError:
                print("Not found config.ini file. Please make config.ini file in config directory")
                exit(0)
        return cls._conf
"""