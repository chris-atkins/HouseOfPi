#!env/bin/python
import os
from flask import Flask


app = Flask(__name__)

app.config.update(dict(
    DEBUG=True
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

wasCalled = False

@app.route('/', methods=['GET'])
def show_entries():
    global wasCalled
    wasCalled = True
    return "Hi"

@app.route('/wasCalled', methods=['GET'])
def was_called():
    global wasCalled
    returnString = str(wasCalled)
    wasCalled = False
    return returnString


app.run(debug=True, host='127.0.0.1', port=3333)