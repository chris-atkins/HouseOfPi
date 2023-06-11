#!env/bin/python
from test_server_setup import buildTestServer
from test_server_setup import ipAddressUrl
from test_server_setup import myHouseUrl
from flask_testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport
import time


class UpdateIpAddressIntegrationTestCase(LiveServerTestCase):

    def create_app(self):
        return buildTestServer(secondsBetweenIpReports='1')

    def test_mock_service_is_up(self):
        response = requests.get(ipAddressUrl)
        self.assertEqual(response.status_code, 200)

    def test_ip_is_updated_with_the_frequency_set_by_config(self):
        expected_sent_request = {
            'houseIp': "https://1.2.3.4:5000"
        }

        time.sleep(2)
        received_data = requests.get(myHouseUrl + '/lastHouseIpPost').json()
        self.assertEqual(received_data, expected_sent_request)

        time.sleep(1)
        received_data = requests.get(myHouseUrl + '/lastHouseIpPost').json()
        self.assertEqual(received_data, expected_sent_request)

