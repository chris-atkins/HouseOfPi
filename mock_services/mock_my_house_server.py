#!env/bin/python
from multiprocessing import Process

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
    return_object = {"message": "Notify stub response"}
    return json.dumps(return_object)


@app.route('/lastNotificationMessage', methods=['GET'])
def get_last_notify_request():
    global lastNotifyRequest
    return_object = lastNotifyRequest
    lastNotifyRequest = None
    return json.dumps(return_object)


@app.route('/house/ip', methods=['POST'])
def post_new_house_ip():
    global last_house_ip
    last_house_ip = request.json
    return json.dumps(request.json)


@app.route('/lastHouseIpPost', methods=['GET'])
def get_last_house_ip_post():
    global last_house_ip
    return_object = last_house_ip
    last_house_ip = '{"message":"no ip post has happened since the last check"}'
    return json.dumps(return_object)


def build_mock_myhouse_server():
    server_process = Process(target=lambda: app.run(debug=True, host='127.0.0.1', port=3333, use_reloader=False))
    server_process.start()
    return server_process
