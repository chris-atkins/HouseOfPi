#!env/bin/python
from test_server_setup import buildTestServer
from test_server_setup import thermostatUrl
from test_server_setup import authenticationSecret
from flask_testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport


class ThermostatIntegrationTestCase(LiveServerTestCase):

    def create_app(self):
        requests.get(thermostatUrl + '/countGETMessages', headers={'auth-secret': authenticationSecret}) #resets the count so previous tests don't interfere
        requests.get(thermostatUrl + '/countNewGETMessages', headers={'auth-secret': authenticationSecret}) #resets the count so previous tests don't interfere
        return buildTestServer()

    def test_mock_service_is_up(self):
        response = requests.get(thermostatUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Server is up')

    def test_set_temp_calls_thermostat_with_correct_values_cool_mode(self):
        current_thermostat_readings = {
            "heattemp": 69.5,
            "cooltemp": 68,
            "mode": 1,
            "spacetemp": 69.5,
            "state": 2,
            "fanstate": 1
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        sent_data = {'targetTemp': 33.45, 'mode': 'COOL'}
        response = requests.post(self.get_server_url() + '/thermostat/state', json=sent_data, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(len(received_data.keys()), 3)
        self.assertEqual(received_data['heattemp'], "69.5")
        self.assertEqual(received_data['cooltemp'], "33.45")
        self.assertEqual(received_data['mode'], "2")

    def test_set_temp_calls_thermostat_with_correct_values_heat_mode(self):
        current_thermostat_readings = {
            "heattemp": 69.5,
            "cooltemp": 68,
            "mode": 2,
            "spacetemp": 69.5,
            "state": 2,
            "fanstate": 1
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        sent_data = {'targetTemp': 72, 'mode': 'HEAT'}
        response = requests.post(self.get_server_url() + '/thermostat/state', json=sent_data, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(len(received_data.keys()), 3)
        self.assertEqual(received_data['heattemp'], "72")
        self.assertEqual(received_data['cooltemp'], "68")
        self.assertEqual(received_data['mode'], "1")

    def test_set_temp_calls_thermostat_with_correct_values_same_mode_from_heat(self):
        current_thermostat_readings = {
            "heattemp": 69.5,
            "cooltemp": 68,
            "mode": 1,
            "spacetemp": 69.5,
            "state": 2,
            "fanstate": 1
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        sent_data = {'targetTemp': 71, 'mode': 'CURRENT'}
        response = requests.post(self.get_server_url() + '/thermostat/state', json=sent_data, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(len(received_data.keys()), 3)
        self.assertEqual(received_data['heattemp'], "71")
        self.assertEqual(received_data['cooltemp'], "68")
        self.assertEqual(received_data['mode'], "1")

    def test_set_temp_calls_thermostat_with_correct_values_same_mode_from_cool(self):
        current_thermostat_readings = {
            "heattemp": 69.5,
            "cooltemp": 68,
            "mode": 2,
            "spacetemp": 69.5,
            "state": 2,
            "fanstate": 1
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        sent_data = {'targetTemp': 66, 'mode': 'CURRENT'}
        response = requests.post(self.get_server_url() + '/thermostat/state', json=sent_data, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(len(received_data.keys()), 3)
        self.assertEqual(received_data['heattemp'], "69.5")
        self.assertEqual(received_data['cooltemp'], "66")
        self.assertEqual(received_data['mode'], "2")

    def test_thermostat_get_endpoint_requires_authentication_header_with_secret(self):
        sent_data = {'a': 'b'}
        response = requests.get(self.get_server_url() + '/house/status', json=sent_data)
        self.assertEqual(response.status_code, 401)

    def test_thermostat_post_endpoint_requires_authentication_header_with_secret(self):
        sent_data = {'targetTemp': 66, 'mode': 'CURRENT'}
        response = requests.post(self.get_server_url() + '/thermostat/state', json=sent_data)
        self.assertEqual(response.status_code, 401)