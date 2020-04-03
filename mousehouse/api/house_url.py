from utils.logger import get_logger
from flask import Blueprint, jsonify
from flask_restful import Resource
from config.config_reader import conf
from .url_api import format_response
from .authentication import authenticate

logger = get_logger(__name__)
class House(Resource):
    """
    House is a monitering server.
    """
    @authenticate
    def get(self):
        """
        Show House information

        Returns:
            Response : Master IP address
        """
        dic = {
            "@url" : "/mousehouse/House",
            "@ip" : conf["master"]["ip"]
        }
        logger.info("Get House IP." )
        return format_response(dic)

class HouseConfig(Resource):
    """
    Config 
    """
    @authenticate
    def get(self):
        """
        Show Config information

        Returns:
            Response : mousehouse configuration.
        """
        def get_config(self):
            """
            Get config parameters.

            Returns:
                list[str] : mousehouse configuration.
            """
            ans = []
            conf_dic = {}
            for i in conf.sections():
                for j in conf[i].keys():
                    conf_dic[j] = conf[i][j]
                ans.append({i:conf_dic})
                conf_dic = {}
            return ans

        conf_dic = get_config(self)
        dic = {
            "@url" : "/mousehouse/House/Config",
            "Config": conf_dic
        }
        logger.debug("Get mousehouse config file." )
        return format_response(dic)
    
    @authenticate
    def post(self):
        """
        Post config

        """

class HouseAction(Resource):
    """
    Action
    """
    @authenticate
    def get(self):
        """
        Show House action
        TODO implement actions

        Returns:
            Response : Power action
        """
        dic = {
            "@url" : "/mousehouse/House/Action",
            "Action" : {
                "Power":"on"
                #"Logservice":"send log",
                #"Script":"id"
            }
        }
        logger.info("Show house action list." )
        return format_response(dic)