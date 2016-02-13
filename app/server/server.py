#!env/bin/python
from flask import Flask  # @UnresolvedImport
from app.hardware.house_of_pi import HouseOfPi

class Server(Flask):

    def __init__(self, name):
        super(Server, self).__init__(name)
        self.hardware = HouseOfPi()

    def run(self, host=None, port=None, debug=None, **options):
        super(Server, self).run(host = host, port = port, debug = debug, **options)
        self.hardwareInterface.start_displaying_on_state()
