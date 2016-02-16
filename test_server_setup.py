#!env/bin/python
from app.server.server import Server
from app.server.api import initRoutes
from app.hardware.house_of_pi import HouseOfPi
from mock_services.test_gpio import TestGPIOFactory

myHouseUrl = 'http://127.0.0.1:3333'

def buildTestServer(track_gpio_calls = False):
    hardware = HouseOfPi(TestGPIOFactory(track_gpio_calls = track_gpio_calls))
    testApp = Server(__name__, hardware)
    
    testApp.config['TESTING'] = True
    testApp.config['LIVESERVER_PORT'] = 8945
    testApp.config['MY_HOUSE_URL'] = 'http://127.0.0.1:3333'
    
    initRoutes(testApp)
    
    return testApp