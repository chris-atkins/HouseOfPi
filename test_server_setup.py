#!env/bin/python
from app.server.server import Server
from app.server.api import initRoutes
from app.hardware.house_of_pi import HouseOfPi

myHouseUrl = 'http://127.0.0.1:3333'

def buildTestServer():
    testApp = Server(__name__, HouseOfPi())
    testApp.config['TESTING'] = True
    testApp.config['LIVESERVER_PORT'] = 8945
    testApp.config['MY_HOUSE_URL'] = 'http://127.0.0.1:3333'
    
    initRoutes(testApp)
    
    return testApp