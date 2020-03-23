from flask import Flask, abort, request, jsonify, Blueprint
from flask_restful import Resource, Api
from .slaveUrl import *
from .masterUrl import *

#mousehouse version
class Root(Resource):
    def get(self):
        return jsonify({
            "@odata.id" : "/mousehouse",
            "Version" : "0.1",
            "Master" : {
                "@odata.id":"/mousehouse/master"
            },
            "Machines" : {
                "@odata.id":"/mousehouse/slaves"
            },
            "LogService" : {
                "@odata.id":"/mousehouse/logservice"
            }
        })

app = Flask(__name__)
api = Api(app, '/mousehouse')
api.add_resource(Root, '/')
#Master's URL
api.add_resource(Master, '/master')
api.add_resource(Status, '/master/status')
api.add_resource(MasterLogs, '/master/masterlogs')

#Machines's URL
api.add_resource(Slaves, '/slaves','/slaves/<int:id>')
#api.add_resource(Slaves, '/slaves/')