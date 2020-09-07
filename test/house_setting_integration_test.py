#!env/bin/python
from flask_testing import LiveServerTestCase
from test_server_setup import buildTestServer

from test_server_setup import thermostatUrl
from test_server_setup import authenticationSecret

import requests


class HouseSettingIntegrationTest(LiveServerTestCase):

    def create_app(self):
        return buildTestServer()

    def test_returns_mode_based_on_thermostat_response_ac(self):
        current_thermostat_readings = {
            "temp": 69.5,
            "tmode": 2,
            "override": 1,
            "hold": 1,
            "t_cool": 68,
            "tstate": 2,
            "fstate": 1
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        response = requests.get(self.get_server_url() + '/house/status', headers={'auth-secret': authenticationSecret})

        expected_response = {
            "mode": "AC",
            "current_temp": 69.5,
            "temp_setting": 68,
            "state": "AC_ON",
            "fan_on": True
        }
        self.assertEqual(expected_response, response.json())

    def test_returns_mode_based_on_thermostat_response_heat(self):
        current_thermostat_readings = {
            "temp": 69,
            "tmode": 1,
            "override": 1,
            "hold": 1,
            "t_heat": 70.5,
            "tstate": 1,
            "fstate": 1
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        response = requests.get(self.get_server_url() + '/house/status', headers={'auth-secret': authenticationSecret})

        expected_response = {
            "mode": "FURNACE",
            "current_temp": 69,
            "temp_setting": 70.5,
            "state": "HEAT_ON",
            "fan_on": True
        }
        self.assertEqual(expected_response, response.json())

    def test_house_endpoint_requires_authentication_header_with_secret(self):
        response = requests.get(self.get_server_url() + '/house/status')
        self.assertEqual(response.status_code, 401)
