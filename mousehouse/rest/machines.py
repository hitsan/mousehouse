import re
from flask import Blueprint, jsonify, make_response, abort
from flask_restful import Resource, request
from utils import logger as lg
from db.dbSetting import session
from db.model.machinesTable import Machine, machine_schema

logger = lg.getLogger(__name__)
class Machines(Resource):
    #logger = lg.getLogger(__name__)
    #ipPattern = r'[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]\.[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]\.[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]\.[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]'
    def get(self):
        all_machines = session.query(Machine)
        return make_response(jsonify({
            "@odata.id":"/mousehouse/machines/",
            "machines" : machine_schema.dump(all_machines)
        }))
            
    def post(self):
        logger.info("POST request")
        rec = request.json
        mach = Machine(ip=rec["ip"], mac=rec["mac"])
        session.add(mach)
        session.commit()

        #return 200

    #def _checkIP(self, ip):
        """
        check ip address normaly and depureccx
        """