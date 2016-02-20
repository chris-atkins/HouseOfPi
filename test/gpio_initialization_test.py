#!env/bin/python
import unittest
from test_server_setup import buildTestServer
from mock_services.test_gpio import GPIOTestFactory

class GpioInitializationTest(unittest.TestCase):

    def setup_class(self):
        self.gpioFactory = GPIOTestFactory(track_gpio_calls = True)
        self.app = buildTestServer(gpioFactory=self.gpioFactory).test_client();

    def test_gpio_pin_scheme_set(self):
        self.assertEqual(self.gpioFactory.getGPIO().gpio_pin_mode_setting(),  'BOARD')
