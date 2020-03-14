from flask import Blueprint, jsonify
from flask_restful import Resource

class Machines(Resource):
    def get(self):
        return jsonify({
            "@odata.id":"/mousehouse/machines/",
            "<id>" : {
                "@odata.id":"/mousehouse/machines/<id>/"
            }
        })
    def post(self):
        #coding post machines
        pass
