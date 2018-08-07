#!env/bin/python
from flask import Flask  # @UnresolvedImport
from flask import request  # @UnresolvedImport
import json

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


lastNotifyRequest = None
last_house_ip = '{"message":"no ip post has happened"}'

@app.route('/', methods=['GET'])
def server_is_up():
    return 'Server is up'

@app.route('/house/notification', methods=['POST'])
def show_entries():
    global lastNotifyRequest
    lastNotifyRequest = request.json
    print(str(lastNotifyRequest))
    returnObject = {"message": "Notify stub response"}
    return json.dumps(returnObject)

@app.route('/lastNotificationMessage', methods=['GET'])
def get_last_notify_request():
    global lastNotifyRequest
    returnObject = lastNotifyRequest
    lastNotifyRequest = None
    return json.dumps(returnObject)

@app.route('/house/ip', methods=['POST'])
def post_new_house_ip():
    global last_house_ip
    last_house_ip = request.json
    return json.dumps(request.json)

@app.route('/lastHouseIpPost', methods=['GET'])
def get_last_house_ip_post():
    global last_house_ip
    returnObject = last_house_ip
    last_house_ip = '{"message":"no ip post has happened since the last check"}'
    return json.dumps(returnObject)

app.run(debug=True, host='127.0.0.1', port=3333)