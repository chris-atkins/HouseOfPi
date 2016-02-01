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

@app.route('/', methods=['GET'])
def server_is_up():
    return 'Server is up'

@app.route('/house/notification', methods=['POST'])
def show_entries():
    global lastNotifyRequest
    lastNotifyRequest = request.json
    print str(lastNotifyRequest)
    returnObject = {"message": "Notify stub response"}
    return json.dumps(returnObject)

@app.route('/lastNotificationMessage', methods=['GET'])
def get_last_notify_request():
    global lastNotifyRequest
    returnObject = lastNotifyRequest
    lastNotifyRequest = None
    return json.dumps(returnObject)


app.run(debug=True, host='127.0.0.1', port=3333)