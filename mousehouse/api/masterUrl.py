from flask import Blueprint, jsonify
from flask_restful import Resource

class Master(Resource):
    def get(self):
        return jsonify({
            "@odata.id" : "/mousehouse/master",
            "Status":{
                "@odata" : "/mousehouse/master/status"
            },
            "IP" : "127.0.0.1",
            "MasterLogs" : {
                "@odata" : "/mousehouse/master/masterlogs"
            }
        })

class Status(Resource):
    def get(self):
        return jsonify({
            "@odata.id" : "/mousehouse/master/status/",
            "Status": "On",
            "Memo" : "If you want to shutdown or reboot, you use POST message."
        })
    def post(self):
        #coding algorym shutdonw or reboot
        pass

class MasterLogs(Resource):
    def get(self):
        return jsonify({
            "@odata" : "/mousehouse/master/masterlogs/"
        })
