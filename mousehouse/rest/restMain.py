from flask import Flask, abort, request, jsonify, Blueprint
from flask_restful import Resource, Api
from . import machines as mc
from . import master as ms

#mousehouse version
class Root(Resource):
    def get(self):
        return jsonify({
            "@odata.id" : "/mousehouse/",
            "Version" : "0.1",
            "Master" : {
                "@odata.id":"/mousehouse/master/"
            },
            "Machines" : {
                "@odata.id":"/mousehouse/machines/"
            },
            "LogService" : {
                "@odata.id":"/mousehouse/logservice/"
            }
        })

app = Flask(__name__)
api = Api(app, '/mousehouse')
api.add_resource(Root, '/')
#Master's URL
api.add_resource(ms.Master, '/master/')
api.add_resource(ms.Status, '/master/status/')
api.add_resource(ms.MasterLogs, '/master/masterlogs/')

#Machines's URL
api.add_resource(mc.Machines, '/machines/')
