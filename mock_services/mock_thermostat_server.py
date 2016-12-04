#!env/bin/python
from flask import Flask  # @UnresolvedImport
from flask import request  # @UnresolvedImport
import json

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


lastThermostatPostRequest = None
thermostatGetCount = 0

@app.route('/', methods=['GET'])
def server_is_up():
    return 'Server is up'

@app.route('/tstat', methods=['GET'])
def get_thermostat_state():
    global thermostatGetCount
    thermostatGetCount += 1
    print('GET thermostat state called n times: ' + str(thermostatGetCount))
    returnObject = {"message": "thermostat stub GET response"}
    return json.dumps(returnObject)

@app.route('/tstat', methods=['POST'])
def post_thermostat_state():
    global lastThermostatPostRequest
    lastThermostatPostRequest = request.json
    print(str(lastThermostatPostRequest))
    return_object = {"message": "Thermostat stub POST response"}
    return json.dumps(return_object)

@app.route('/countGETMessages', methods=['GET'])
def get_last_temp_check_request():
    global thermostatGetCount
    return_object = {"count": thermostatGetCount}
    return json.dumps(return_object)

@app.route('/lastPOSTMessage', methods=['GET'])
def get_last_change_heat_request():
    global lastThermostatPostRequest
    return_object = lastThermostatPostRequest
    lastThermostatPostRequest = None
    return json.dumps(return_object)


app.run(debug=True, host='127.0.0.1', port=4444)