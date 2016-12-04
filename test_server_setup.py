#!env/bin/python
from app.server.server import Server
from app.server.api import initRoutes
from app.hardware.house_of_pi import HouseOfPi
from mock_services.test_gpio import GPIOTestFactory

myHouseUrl = 'http://127.0.0.1:3333'
thermostatUrl = 'http://127.0.0.1:4444'

def buildTestServer(track_gpio_calls = False, gpioFactory=None):
    if gpioFactory == None:
        gpioFactory = GPIOTestFactory(track_gpio_calls = track_gpio_calls) 
    hardware = HouseOfPi(gpioFactory)
    testApp = Server(__name__, hardware)
    
    testApp.config['TESTING'] = True
    testApp.config['LIVESERVER_PORT'] = 8945
    testApp.config['MY_HOUSE_URL'] = myHouseUrl
    testApp.config['THERMOSTAT_URL'] = thermostatUrl
    
    initRoutes(testApp)
    
    return testApp