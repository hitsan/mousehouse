import os
import sys
import configparser
import subprocess

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
            path = os.path.abspath(__file__)
            config_path = path[:-32] + 'config/config.ini'
            self._conf.read(config_path, encoding='utf-8')
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