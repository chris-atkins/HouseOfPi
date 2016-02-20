#!env/bin/python
import unittest
from test_server_setup import buildTestServer
from mock_services.test_gpio import GPIOTestFactory
import time

class WinkEndpointTest(unittest.TestCase):

    def setup_class(self):
        self.gpio_factory = GPIOTestFactory( track_gpio_calls = False)
        self.app = buildTestServer(gpioFactory=self.gpio_factory).test_client()

    def test_gpio_blinks_twenty_times_in_twenty_seconds(self):
        response = self.app.get('/wink')
        self.assertEqual(response.status_code, 200)
        time.sleep(2)
        self.assertEqual(self.gpio_factory.getGPIO().number_of_high_calls_for_channel(11), 20)
        self.assertEqual(self.gpio_factory.getGPIO().number_of_low_calls_for_channel(11), 20)
        