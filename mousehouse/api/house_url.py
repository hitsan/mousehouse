from utils.logger import get_logger
from flask import Blueprint, jsonify
from flask_restful import Resource
from config.config_reader import conf
from .url_api import format_response

logger = get_logger(__name__)
class House(Resource):
    """
    House is a monitering server.
    """
    def get(self):
        """
        Show House information
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
    def get(self):
        """
        Show Config information
        """
        def get_config(self, con):
            """
            Get config parameters.
            """
            ans = []
            conf_dic = {}
            for i in con.sections():
                for j in conf[i].keys():
                    conf_dic[j] = conf[i][j]
                ans.append({i:conf_dic})
                conf_dic = {}
            return ans
        conf_dic = get_config(self, conf)
        dic = {
            "@url" : "/mousehouse/House/Config",
            "Config": conf_dic
        }
        logger.debug("Get mousehouse config file." )
        return format_response(dic)
    
    def post(self):
        """
        Post config
        """

class HouseAction(Resource):
    def get(self):
        """
        Show House action
        TODO implement actions
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