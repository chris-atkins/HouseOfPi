#!env/bin/python
from app.server.server import Server
from app.server.api import initRoutes
from app.server.scheduled_jobs import init_scheduled_jobs
from app.hardware.house_of_pi import HouseOfPi
from mock_services.test_gpio import GPIOTestFactory

myHouseUrl='http://127.0.0.1:3333'
thermostatUrl='http://127.0.0.1:4444'
lightsUrl='http://127.0.0.1:5555'
ipAddressUrl='http://127.0.0.1:6234'
secondsBetweenIpReports='300'
authenticationSecret="oh hi guess who it is"


class MockWemo(object):

    last_brightness = -1

    def set_brightness(self, brightness):
        MockWemo.last_brightness = brightness

    def get_brightness(self):
        return MockWemo.last_brightness


def buildTestServer(track_gpio_calls=False,
                    gpioFactory=None,
                    myHouseUrl=myHouseUrl,
                    thermostatUrl=thermostatUrl,
                    lightsUrl=lightsUrl,
                    ipAddressUrl=ipAddressUrl,
                    secondsBetweenIpReports=secondsBetweenIpReports,
                    authenticationSecret=authenticationSecret,
                    motion_sensing_cycle_time=.1,
                    wemoDevices=[]):

    if gpioFactory == None:
        gpioFactory = GPIOTestFactory(track_gpio_calls = track_gpio_calls)
    hardware = HouseOfPi(gpioFactory, motion_sensing_cycle_time = motion_sensing_cycle_time)
    testApp = Server(__name__, hardware, wemoDevices)
    
    testApp.config['TESTING'] = True
    testApp.config['LIVESERVER_PORT'] = 8945
    testApp.config['MY_HOUSE_URL'] = myHouseUrl
    testApp.config['THERMOSTAT_URL'] = thermostatUrl
    testApp.config['LIGHTS_URL'] = lightsUrl
    testApp.config['IP_ADDRESS_URL'] = ipAddressUrl
    testApp.config['SECONDS_BETWEEN_IP_REPORTS'] = secondsBetweenIpReports
    testApp.config['AUTHENTICATION_SECRET'] = authenticationSecret

    initRoutes(testApp)
    init_scheduled_jobs(testApp.config)

    return testApp