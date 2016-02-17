#!env/bin/python

from test_server_setup import buildTestServer
from flask.ext.testing import LiveServerTestCase  # @UnresolvedImport
import test.helper as testHelper

class GpioInitializationTest(LiveServerTestCase):
    
    def create_app(self):
        return buildTestServer(track_gpio_calls = True)
    
    def test_gpio_pin_scheme_set(self):
        gpio = testHelper.load_tracked_gpio();
        self.assertEqual(gpio.gpio_pin_mode_setting(),  'BOARD')