from utils.logger import get_logger
from flask import Blueprint, jsonify
from flask_restful import Resource
from utils.config_reader import conf
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