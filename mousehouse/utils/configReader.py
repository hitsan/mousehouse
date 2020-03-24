import os
import sys
import configparser

class ConfigReader:
    """
    Read the config.ini and generate a configuration reference.
    """
    def __init__(self):
        """
        Read the config.ini
        """
        self._conf = configparser.ConfigParser()
        try:
            home = os.environ['mousehouse_home']
            configPath =  home + '/config/config.ini'
            self._conf.read(configPath, encoding='utf-8')
        except KeyError:  
            print("Please set mousehouse_home", file=sys.stderr)
            exit(0)
        except TypeError:
            print("Not found config.ini file. Please make config.ini file in config directory", file=sys.stderr)
            exit(0)

    @property
    def getConfig(self):
        """
        Retrun the configuration reference
        """
        return self._conf

conf = ConfigReader().getConfig