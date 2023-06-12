#!env/bin/python
from flask import Flask  # @UnresolvedImport
from flask import request  # @UnresolvedImport
from flask import Response  # @UnresolvedImport
from multiprocessing import Process
import json

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

lastThermostatStatePostRequest = None
mockResponseToReturnForGetStatus = None
thermostatGetCount = 0


@app.route('/', methods=['GET'])
def server_is_up():
    return 'Server is up'


@app.route('/query/info', methods=['GET'])
def get_new_thermostat_state():
    global thermostatGetCount
    global mockResponseToReturnForGetStatus
    thermostatGetCount += 1
    return_object = {"message": "thermostat stub GET response"}
    print("got a request and mock response is set to ", mockResponseToReturnForGetStatus)
    if mockResponseToReturnForGetStatus is not None:
        return_object = mockResponseToReturnForGetStatus
        mockResponseToReturnForGetStatus = None
    return json.dumps(return_object)


@app.route('/query/info/set-mock', methods=['POST'])
def set_new_mock_thermostat_state_response():
    global mockResponseToReturnForGetStatus
    print("saved response ", request.json)
    mockResponseToReturnForGetStatus = request.json
    return Response(status=200)


@app.route('/control', methods=['POST'])
def post_thermostat_state():
    global lastThermostatStatePostRequest
    lastThermostatStatePostRequest = request.form
    print(str(request.content_type))
    if request.content_type != "application/x-www-form-urlencoded":
        return Response('Expecting content type application/x-www-form-urlencoded :(', 420)
    return_object = {"success": True}
    return json.dumps(return_object)


@app.route('/countGETMessages', methods=['GET'])
def get_last_new_temp_check_request():
    global thermostatGetCount
    return_object = {"count": thermostatGetCount}
    thermostatGetCount = 0
    return json.dumps(return_object)


@app.route('/lastThermostatStatePostRequest', methods=['GET'])
def get_last_change_thermostat_state_post_request():
    global lastThermostatStatePostRequest
    response = {}
    for key in lastThermostatStatePostRequest.keys():
        response[key] = float(lastThermostatStatePostRequest[key])

    lastThermostatStatePostRequest = None
    return json.dumps(response)


def build_mock_thermostat_server():
    server_process = Process(target=lambda: app.run(debug=False, host='127.0.0.1', port=4444, use_reloader=False))
    server_process.start()
    return server_process
