#!env/bin/python
from app.server.hardware_interface import HardwareInterface 

class HouseOfPi(HardwareInterface):

    def __init__(self):
        super(HouseOfPi, self).__init__()
        
    def start_displaying_on_state(self):
        pass
        