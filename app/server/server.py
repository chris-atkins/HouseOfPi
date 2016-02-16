#!env/bin/python
from flask import Flask  # @UnresolvedImport
from app.hardware import app_status_display

class Server(Flask):

    def __init__(self, name, hardwareInterface):
        super(Server, self).__init__(name)
        self.hardware = hardwareInterface

    def run(self, host=None, port=None, debug=None, **options):
        self.hardware.start_displaying_on_state()
        app_status_display.start_server_on_display_every(2)
        super(Server, self).run(host = host, port = port, debug = debug, **options)
