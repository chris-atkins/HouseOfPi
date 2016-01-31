#!env/bin/python
from flask import Flask  # @UnresolvedImport


app = Flask(__name__)
app.config.update(dict(
    DEBUG=True
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


notifyWasCalled = False

@app.route('/', methods=['GET'])
def server_is_up():
    return 'Server is up'

@app.route('/house/notify', methods=['GET'])
def show_entries():
    global notifyWasCalled
    notifyWasCalled = True
    return "Notify stub response"

@app.route('/notifyWasCalled', methods=['GET'])
def was_called():
    global notifyWasCalled
    returnString = str(notifyWasCalled)
    notifyWasCalled = False
    return returnString


app.run(debug=True, host='127.0.0.1', port=3333)