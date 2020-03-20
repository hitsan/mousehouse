import re
from flask import Blueprint, jsonify
from flask_restful import Resource, request
from utils import logger as lg
from db import dbManager

class Machines(Resource):
    logger = lg.getLogger(__name__)
    #ipPattern = r'[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]\.[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]\.[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]\.[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]'
    def get(self):
        return jsonify({
            "@odata.id":"/mousehouse/machines/",
            "<id>" : {
                "@odata.id":"/mousehouse/machines/<id>/"
            }
        })
            #message = json.dumps({'errors': errors})
            #return Response(message, status=422, mimetype='application/json')
    def post(self):
        self.logger.info("POST request")
        machine = request.json
        if not list(machine.keys()) == ['ip', 'mac_address']:
            return "Invalid"
        cur.execute('INSERT INTO msDB (ip, macAdrr) VALUES (%s, %s)', machine['ip'], machine['mac_address'])
        """
        print(machine["ip"])
        if re.match(self.ipPattern, machine["ip"]) is None:
            return "invaild IP Address"
        return "true"
        """
        
