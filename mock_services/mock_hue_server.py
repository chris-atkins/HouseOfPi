#!env/bin/python
from flask import Flask  # @UnresolvedImport
from flask import request  # @UnresolvedImport
import json

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


last_lights_put_request = None

@app.route('/', methods=['GET'])
def server_is_up():
    return 'Server is up'

@app.route('/api/6b1abf1f6e7157cc3843ee8b668d32d/groups/0/action', methods=['PUT'])
def change_lights():
    global last_lights_put_request
    last_lights_put_request = request.json
    return_object = {"message": "Lights stub PUT response"}
    return json.dumps(return_object)


@app.route('/lastPUTMessage', methods=['GET'])
def get_last_change_lights_request():
    global last_lights_put_request
    return_object = last_lights_put_request
    last_lights_put_request = None
    return json.dumps(return_object)


app.run(debug=True, host='127.0.0.1', port=5555)