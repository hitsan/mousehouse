import re
from flask import Blueprint, jsonify
from flask_restful import Resource, request
from utils import logger as lg
from db.dbSetting import session
from db.model.machinesTable import Machine

logger = lg.getLogger(__name__)
class Machines(Resource):
    #logger = lg.getLogger(__name__)
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
        logger.info("POST request")
        rec = request.json
        mach = Machine(ip_addr=rec["ip"], mac_addr=rec["mac_address"])
        session.add(mach)
        session.commit()

        #return 200

        #cur.execute('INSERT INTO msDB (ip, macAdrr) VALUES (%s, %s)', machine['ip'], machine['mac_address'])
    #def _checkIP(self, ip):
        """
        check ip address normaly and depureccx
        """