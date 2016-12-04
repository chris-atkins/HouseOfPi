#!env/bin/python
from test_server_setup import buildTestServer
from test_server_setup import thermostatUrl
from flask.ext.testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport

class ThermostatIntegrationTestCase(LiveServerTestCase):

    def create_app(self):
        return buildTestServer()

    def test_mock_service_is_up(self):
        response = requests.get(thermostatUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Server is up')

    def test_get_on_thermostat_endpoint_calls_thermostat(self):
        response = requests.get(self.get_server_url() + '/tstat')
        self.assertEquals(response.status_code, 200)

        count_messages_response = requests.get(thermostatUrl + '/countGETMessages')
        count = count_messages_response.json()['count']
        self.assertEquals(count, 1)

    def test_get_on_thermostat_endpoint_returns_same_response_as_thermostat(self):
        response = requests.get(self.get_server_url() + '/tstat')
        self.assertEquals(response.status_code, 200)

        expected_response = {"message": "thermostat stub GET response"}
        self.assertEquals(response.json(), expected_response)

    def test_set_temp_calls_thermostat_with_same_request(self):
        sent_data = {'a': 'b'}
        response = requests.post(self.get_server_url() + '/tstat', json=sent_data)
        self.assertEquals(response.status_code, 200)

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEquals(received_data, sent_data)

    def test_set_temp_returns_response_from_thermostat(self):
        sent_data = {'a': 'b'}
        response = requests.post(self.get_server_url() + '/tstat', json=sent_data)
        self.assertEquals(response.status_code, 200)

        expected_response = {"message": "Thermostat stub POST response"}
        self.assertEquals(response.json(), expected_response)
