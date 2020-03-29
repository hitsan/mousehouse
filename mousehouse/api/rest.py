from flask import Flask, abort, request, jsonify, Blueprint
from flask_restful import Resource, Api
from .url_api import format_response
from .mice_url import *
from .house_url import *

class Root(Resource):
    """
    mousehouse information
    
    """
    def get(self):
        """
        Get mousehouse information
        """
        dic = {
            "@url" : "/mousehouse",
            "Version" : "0.1",
            "Master" : {
                "@url":"/mousehouse/House"
            },
            "Slave" : {
                "@url":"/mousehouse/Mice"
            }
        }
        return format_response(dic)

app = Flask(__name__)
api = Api(app, '/mousehouse')
api.add_resource(Root, '')
"""
Master's URL
"""
api.add_resource(House, '/House')
api.add_resource(HouseConfig, '/House/Config')
api.add_resource(HouseAction, '/House/Action')

"""
Slaves's URL
"""
api.add_resource(Mice, '/Mice','/Mice/<int:id>')
api.add_resource(MiceAction, '/Mice/<int:id>/Action')
api.add_resource(MicePower, '/Mice/<int:id>/Action/Power')
