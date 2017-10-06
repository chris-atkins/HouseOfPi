#!env/bin/python
from test_server_setup import buildTestServer
from test_server_setup import lightsUrl
from test_server_setup import authenticationSecret
from flask.ext.testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport

class HouseCommandIntegrationTestCase(LiveServerTestCase):

    def create_app(self):
        return buildTestServer()

    def test_mock_service_is_up(self):
        response = requests.get(lightsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Server is up')

    def test_house_endpoint_requires_authentication_header_with_secret(self):
        request_json = {'a': 'b'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json)
        self.assertEqual(response.status_code, 401)

    def test_house_mode_lights_on_sends_correct_request_to_hue(self):
        request_json = {'command': 'lights-on'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': True,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert':'none',
            'xy': [0.3852,0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEquals(received_data, expected_sent_request)

    def test_house_mode_lights_off_sends_correct_request_to_hue(self):
        request_json = {'command': 'lights-off'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': False,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert':'none',
            'xy': [0.3852,0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEquals(received_data, expected_sent_request)

    def test_house_mode_at_work_sends_correct_requests_to_hue(self):
        request_json = {'command': 'at-work-mode'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status': 'success'})

        expected_other_light_request = {
            'on': False,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert':'none',
            'xy': [0.3852,0.3815]
        }
        expected_plant_light_request = {
            'on': True,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert':'none',
            'xy': [0.3852,0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/1').json()
        self.assertEquals(received_data, expected_other_light_request)

        received_data = requests.get(lightsUrl + '/lastPUTMessage/2').json()
        self.assertEquals(received_data, expected_plant_light_request)


    def test_house_mode_outside_lights_off_sends_correct_request_to_hue(self):
        request_json = {'command': 'outside-lights-off'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': False,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert':'none',
            'xy': [0.3852,0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/3').json()
        self.assertEquals(received_data, expected_sent_request)

    def test_house_mode_outside_lights_on_sends_correct_request_to_hue(self):
        request_json = {'command': 'outside-lights-on'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': True,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert':'none',
            'xy': [0.3852,0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/3').json()
        self.assertEquals(received_data, expected_sent_request)
