#!env/bin/python
from multiprocessing import Process

from flask import Flask  # @UnresolvedImport
from flask import request  # @UnresolvedImport


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


def build_mock_ip_address_server():
    server_process = Process(target=lambda: app.run(host='127.0.0.1', port=6234, debug=True, use_reloader=False))
    server_process.start()
    return server_process
