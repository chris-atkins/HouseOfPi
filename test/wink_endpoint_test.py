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
import test.helper as testHelper
from flask_testing import LiveServerTestCase  # @UnresolvedImport


class WinkEndpointTest(LiveServerTestCase):

    def create_app(self):
        return buildTestServer(track_gpio_calls = True)

    def test_gpio_blinks_twenty_times_in_twenty_seconds(self):
        response = requests.get(self.get_server_url() + '/wink', headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)

        time.sleep(2.2)

        gpio = testHelper.load_tracked_gpio()
        self.assertEqual(gpio.number_of_high_calls_for_channel(13), 20)

        # uses greater than because the motion sensor calls LOW on the same channel and the actual number is a little different each time
        self.assertTrue(gpio.number_of_low_calls_for_channel(13) > 20)

    def test_wink_endpoint_requires_authentication_header_with_secret(self):
        response = requests.get(self.get_server_url() + '/wink')
        self.assertEqual(response.status_code, 401)

    def test_wink_endpoint_with_no_auth_sends_text(self):
        requests.get(self.get_server_url() + '/wink')
        sentText = requests.get(myHouseUrl + '/lastNotificationMessage').text

        expectedPartialTextContent = "An unauthorized request was made to the House of Pi application:"
        self.assertIn(expectedPartialTextContent, sentText)

    def test_wink_endpoint_with_bad_auth_sends_text(self):
        requests.get(self.get_server_url() + '/wink', headers={'auth-secret': 'bad Secret that is wrong'})
        sentText = requests.get(myHouseUrl + '/lastNotificationMessage').text

        expectedPartialTextContent = "An unauthorized request was made to the House of Pi application:"
        self.assertIn(expectedPartialTextContent, sentText)

