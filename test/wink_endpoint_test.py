#!env/bin/python

# noinspection PyUnresolvedReferences
import time
# noinspection PyUnresolvedReferences
import requests
# noinspection PyUnresolvedReferences
import unittest

from test_server_setup import buildTestServer
from test_server_setup import authenticationSecret
from test_server_setup import myHouseUrl
from mock_services.test_gpio import GPIOTestFactory


class WinkEndpointTest(unittest.TestCase):

    def setup_class(self):
        self.gpio_factory = GPIOTestFactory( track_gpio_calls = False)
        self.app = buildTestServer(gpioFactory=self.gpio_factory).test_client()

    def test_gpio_blinks_twenty_times_in_twenty_seconds(self):
        response = self.app.get('/wink', headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        time.sleep(2.2)
        self.assertEqual(self.gpio_factory.getGPIO().number_of_high_calls_for_channel(13), 20)
        self.assertEqual(self.gpio_factory.getGPIO().number_of_low_calls_for_channel(13), 20)

    def test_wink_endpoint_requires_authentication_header_with_secret(self):
        response = self.app.get('/wink')
        self.assertEqual(response.status_code, 401)

    def test_wink_endpoint_with_no_auth_sends_text(self):
        self.app.get('/wink')
        sentText = requests.get(myHouseUrl + '/lastNotificationMessage').text

        expectedPartialTextContent = "An unauthorized request was made to the House of Pi application:"
        self.assertIn(expectedPartialTextContent, sentText)

    def test_wink_endpoint_with_bad_auth_sends_text(self):
        self.app.get('/wink', headers={'auth-secret': 'bad Secret that is wrong'})
        sentText = requests.get(myHouseUrl + '/lastNotificationMessage').text

        expectedPartialTextContent = "An unauthorized request was made to the House of Pi application:"
        self.assertIn(expectedPartialTextContent, sentText)

