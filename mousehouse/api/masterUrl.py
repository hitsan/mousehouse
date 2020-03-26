from flask import Blueprint, jsonify
from flask_restful import Resource
from utils.configReader import conf

class Master(Resource):
    """
    Master is a monitering server.
    """
    def get(self):
        """
        Show Master information
        """
        return jsonify({
            "@url" : "/mousehouse/Master",
            "@ip" : conf["master"]["ip"]
        })

class MasterAction(Resource):
    def get(self):
        """
        Show Master action
        TODO implement actions
        """
        return jsonify({
            "@url" : "/mousehouse/Master/Action",
            "Action" : {
                "Power":"on"
                #"Logservice":"send log",
                #"Script":"id"
            }
        })