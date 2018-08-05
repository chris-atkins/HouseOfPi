#!env/bin/python
from test_server_setup import buildTestServer
from test_server_setup import lightsUrl
from test_server_setup import authenticationSecret
from flask_testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport

class LightsIntegrationTestCase(LiveServerTestCase):

    def create_app(self):
        return buildTestServer()

    def test_mock_service_is_up(self):
        response = requests.get(lightsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Server is up')

    def test_put_lights_calls_lights_server_with_same_request(self):
        sent_data = {'a': 'b'}
        response = requests.put(self.get_server_url() + '/lights/state', json=sent_data, headers={'auth-secret': authenticationSecret})
        self.assertEquals(response.status_code, 200)

        received_data = requests.get(lightsUrl + '/lastPUTMessage').json()
        self.assertEquals(received_data, sent_data)

    def test_put_lights_returns_response_from_lights_server(self):
        sent_data = {'a': 'b'}
        response = requests.put(self.get_server_url() + '/lights/state', json=sent_data, headers={'auth-secret': authenticationSecret})
        self.assertEquals(response.status_code, 200)

        expected_response = {"message": "Lights stub PUT response"}
        self.assertEquals(response.json(), expected_response)

    def test_lights_endpoint_requires_authentication_header_with_secret(self):
        sent_data = {'a': 'b'}
        response = requests.put(self.get_server_url() + '/lights/state', json=sent_data)
        self.assertEqual(response.status_code, 401)
