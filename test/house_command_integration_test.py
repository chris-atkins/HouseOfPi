#!env/bin/python
from test_server_setup import buildTestServer
from test_server_setup import lightsUrl
from test_server_setup import thermostatUrl
from test_server_setup import authenticationSecret
from flask_testing import LiveServerTestCase
import requests


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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': True,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEqual(received_data, expected_sent_request)

    def test_house_mode_lights_dim_sends_correct_request_to_hue(self):
        request_json = {'command': 'dim-lights'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': True,
            'bri': 73,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEqual(received_data, expected_sent_request)

    def test_house_mode_basement_dim_sends_correct_request_to_hue(self):
        request_json = {'command': 'basement-dim'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': True,
            'bri': 73,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/8').json()
        self.assertEqual(received_data, expected_sent_request)

    def test_house_mode_basement_on_sends_correct_request_to_hue(self):
        request_json = {'command': 'basement-on'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': True,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/8').json()
        self.assertEqual(received_data, expected_sent_request)

    def test_house_mode_basement_of_sends_correct_request_to_hue(self):
        request_json = {'command': 'basement-off'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': False,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/8').json()
        self.assertEqual(received_data, expected_sent_request)

    def test_house_mode_lights_off_sends_correct_request_to_hue(self):
        request_json = {'command': 'lights-off'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': False,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEqual(received_data, expected_sent_request)

    def test_house_mode_at_work_sends_correct_requests_from_furnace_mode(self):
        current_thermostat_readings = {
            "temp": 69.5,
            "tmode": 1,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_heat": 70,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'at-work-mode'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_inside_light_request = {
            'on': False,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        expected_plant_light_request = {
            'on': True,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        expected_heat_request = {
            't_heat': 64.0,
            'tmode': 1,
            'hold': 1
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEqual(received_data, expected_inside_light_request)

        received_data = requests.get(lightsUrl + '/lastPUTMessage/2').json()
        self.assertEqual(received_data, expected_plant_light_request)

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_house_mode_at_work_sends_correct_requests_from_AC_mode(self):
        current_thermostat_readings = {
            "temp": 69.5,
            "tmode": 2,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_cool": 68,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'at-work-mode'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_indoor_light_request = {
            'on': False,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        expected_plant_light_request = {
            'on': True,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        expected_heat_request = {
            't_cool': 70.0,
            'tmode': 2,
            'hold': 1
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEqual(received_data, expected_indoor_light_request)

        received_data = requests.get(lightsUrl + '/lastPUTMessage/2').json()
        self.assertEqual(received_data, expected_plant_light_request)

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_house_mode_outside_lights_off_sends_correct_request_to_hue(self):
        request_json = {'command': 'outside-lights-off'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': False,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/3').json()
        self.assertEqual(received_data, expected_sent_request)

    def test_house_mode_outside_lights_on_sends_correct_request_to_hue(self):
        request_json = {'command': 'outside-lights-on'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': True,
            'bri': 254,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/3').json()
        self.assertEqual(received_data, expected_sent_request)

    def test_temp_down_command_with_AC_on_and_temp_more_than_2_above_min(self):
        current_thermostat_readings = {
            "temp": 69.5,
            "tmode": 2,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_cool": 70,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": 67.5
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_cool': 67.5,
            'tmode': 2,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_down_command_with_AC_on_and_temp_less_than_2_above_min(self):
        current_thermostat_readings = {
            "temp": 67.5,
            "tmode": 2,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_cool": 70,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": 67
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_cool': 67,
            'tmode': 2,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_down_command_with_AC_on_and_temp_already_at_min(self):
        current_thermostat_readings = {
            "temp": 67,
            "tmode": 2,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_cool": 70,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "no-change",
            "temperature-mode": "AC",
            "target-temp": 67
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_cool': 67,
            'tmode': 2,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_down_command_with_AC_on_and_temp_less_than_min(self):
        current_thermostat_readings = {
            "temp": 65,
            "tmode": 2,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_cool": 65,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "no-change",
            "temperature-mode": "AC",
            "target-temp": 67
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_cool': 67,
            'tmode': 2,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_down_command_with_Furnace_on(self):
        current_thermostat_readings = {
            "temp": 65,
            "tmode": 1,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_heat": 73,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "furnace",
            "target-temp": 63
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_heat': 63,
            'tmode': 1,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_up_command_with_Furnace_on_and_temp_more_than_2_below_max(self):
        current_thermostat_readings = {
            "temp": 66.5,
            "tmode": 1,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_heat": 66,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-up'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-up",
            "result": "success",
            "temperature-mode": "furnace",
            "target-temp": 68.5
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_heat': 68.5,
            'tmode': 1,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_up_command_with_furnace_on_and_temp_less_than_2_below_max(self):
        current_thermostat_readings = {
            "temp": 71.5,
            "tmode": 1,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_heat": 70,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-up'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-up",
            "result": "success",
            "temperature-mode": "furnace",
            "target-temp": 72
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_heat': 72,
            'tmode': 1,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_up_command_with_furnace_on_and_temp_already_at_max(self):
        current_thermostat_readings = {
            "temp": 72,
            "tmode": 1,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_heat": 70,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-up'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-up",
            "result": "no-change",
            "temperature-mode": "furnace",
            "target-temp": 72
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_heat': 72,
            'tmode': 1,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_up_command_with_furnace_on_and_temp_above_max(self):
        current_thermostat_readings = {
            "temp": 92,
            "tmode": 1,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_heat": 72,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-up'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-up",
            "result": "no-change",
            "temperature-mode": "furnace",
            "target-temp": 72
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_heat': 72,
            'tmode': 1,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)

    def test_temp_up_command_with_AC_on(self):
        current_thermostat_readings = {
            "temp": 65,
            "tmode": 2,
            "fmode": 0,
            "override": 1,
            "hold": 1,
            "t_cool": 73,
            "tstate": 2,
            "fstate": 1,
            "time": {
                "day": 6,
                "hour": 14,
                "minute": 51
            },
            "t_type_post": 0
        }
        requests.post(thermostatUrl + "/tstat/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-up'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-up",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": 67
        }
        self.assertEqual(response.json(), expected_response)

        expected_heat_request = {
            't_cool': 67,
            'tmode': 2,
            'hold': 1
        }

        received_data = requests.get(thermostatUrl + '/lastPOSTMessage').json()
        self.assertEqual(received_data, expected_heat_request)
