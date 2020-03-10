from flask import Blueprint, request

app = Blueprint('manager', __name__)

@app.route('/', method=['GET'])
def getConfig():
    return 'tea'