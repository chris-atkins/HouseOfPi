#!env/bin/python
from flask import Flask  # @UnresolvedImport
from flask import request  # @UnresolvedImport
import json

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/', methods=['GET'])
def ip_address():
    if request.args.get('format') == 'json':
        return '{"ip": "1.2.3.4"}'
    return '{"ip":"no query params for format=json were in the request"}'

app.run(debug=True, host='127.0.0.1', port=6234)
