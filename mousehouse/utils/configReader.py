import configparser
import os    

class ConfigReader:
    _config_reader = None
    _conf = None
    def __new__(cls):
        if cls._config_reader is None:
            cls._config_reader = super().__new__(cls)
        return cls._config_reader

    @classmethod
    def getConfig(cls):
        #return cls._config_reader
        if cls._conf is None:
            cls._conf = configparser.ConfigParser()
            try:
                home = os.environ['mousehouse_home']
                config_path =  home + '/config/config.ini'
                cls._conf.read(config_path, encoding='utf-8')
            except KeyError as e:  
                print("Please set mousehouse_home")
                exit(0)
            except TypeError:
                print("Not found config.ini file. Please make config.ini file in config directory")
                exit(0)
        return cls._conf
