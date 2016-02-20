#!env/bin/python
from flask import Flask  # @UnresolvedImport

class Server(Flask):

    def __init__(self, name, hardwareInterface):
        super(Server, self).__init__(name)
        self.hardware = hardwareInterface

    def run(self, host=None, port=None, debug=None, **options):
        self.init_hardware()
        super(Server, self).run(host = host, port = port, debug = debug, **options)
        
    def init_hardware(self):
        self.hardware.start_displaying_on_state()