from flask import Flask, abort, request, jsonify, Blueprint
from flask_restful import Resource, Api
from .slave_url import *
from .master_url import *

class Root(Resource):
    """
    mousehouse information
    
    """
    def get(self):
        """
        Get mousehouse information
        """
        return jsonify({
            "@odata.id" : "/mousehouse",
            "Version" : "0.1",
            "Master" : {
                "@odata.id":"/mousehouse/Master"
            },
            "Machines" : {
                "@odata.id":"/mousehouse/Slaves"
            }
        })

app = Flask(__name__)
api = Api(app, '/mousehouse')
api.add_resource(Root, '')
"""
Master's URL
"""
api.add_resource(Master, '/Master')
api.add_resource(MasterAction, '/Master/Action')

"""
Slaves's URL
"""
api.add_resource(Slaves, '/Slaves','/Slaves/<int:id>')
api.add_resource(SlaveAction, '/Slaves/<int:id>/Action')
api.add_resource(SlavePower, '/Slaves/<int:id>/Action/Power')
