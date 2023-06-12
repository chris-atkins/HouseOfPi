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

    def setUp(self):
        requests.get(thermostatUrl + '/countGETMessages')  # resets count to zero so each test can be isolated from others

    def assertNoInteractionsWithThermostat(self):
        response = requests.get(thermostatUrl + '/countGETMessages')
        get_count = response.json()['count']
        self.assertEqual(get_count, 0)

        response = requests.get(thermostatUrl + '/lastThermostatStatePostRequest')
        self.assertEqual(len(response.json().keys()), 0)

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
        self.assertNoInteractionsWithThermostat()

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
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_basement_dim_sends_correct_request_to_hue(self):
        request_json = {'command': 'basement-dim'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_dim_request = {
            'on': True,
            'bri': 73,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        expected_off_request = {
            'on': False,
            'bri': 73,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/11').json()
        self.assertEqual(received_data, expected_dim_request)
        received_data = requests.get(lightsUrl + '/lastPUTMessage/10').json()
        self.assertEqual(received_data, expected_off_request)
        self.assertNoInteractionsWithThermostat()

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
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_basement_off_sends_correct_request_to_hue(self):
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
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_bedroom_on_sends_correct_request_to_hue(self):
        request_json = {'command': 'bedroom-on'}
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
        received_data = requests.get(lightsUrl + '/lastPUTMessage/5').json()
        self.assertEqual(received_data, expected_sent_request)
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_bedroom_off_sends_correct_request_to_hue(self):
        request_json = {'command': 'bedroom-off'}
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
        received_data = requests.get(lightsUrl + '/lastPUTMessage/5').json()
        self.assertEqual(received_data, expected_sent_request)
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_fancy_light_on_sends_correct_request_to_hue(self):
        request_json = {'command': 'fancy-light-on'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        expected_sent_request = {
            'on': True,
            'bri': 128,
            'hue': 19228,
            'sat': 13,
            'ct': 257,
            'effect': 'none',
            'alert': 'none',
            'xy': [0.3852, 0.3815]
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/13').json()
        self.assertEqual(received_data, expected_sent_request)
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_fancy_light_off_sends_correct_request_to_hue(self):
        request_json = {'command': 'fancy-light-off'}
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
        received_data = requests.get(lightsUrl + '/lastPUTMessage/13').json()
        self.assertEqual(received_data, expected_sent_request)
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_plant_lights_on_sends_correct_request_to_hue(self):
        request_json = {'command': 'plant-lights-on'}
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
        received_data = requests.get(lightsUrl + '/lastPUTMessage/14').json()
        self.assertEqual(received_data, expected_sent_request)
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_plant_lights_off_sends_correct_request_to_hue(self):
        request_json = {'command': 'plant-lights-off'}
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
        received_data = requests.get(lightsUrl + '/lastPUTMessage/14').json()
        self.assertEqual(received_data, expected_sent_request)
        self.assertNoInteractionsWithThermostat()

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
        self.assertNoInteractionsWithThermostat()

    def test_house_mode_at_work_sends_correct_requests_from_furnace_mode(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 50,
            "mode": 1,
            "spacetemp": 69
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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
        expected_thermostat_request = {
            'mode': 1,
            'heattemp': 64,
            'cooltemp': 50
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEqual(received_data, expected_inside_light_request)

        received_data = requests.get(lightsUrl + '/lastPUTMessage/2').json()
        self.assertEqual(received_data, expected_plant_light_request)

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_house_mode_at_work_sends_correct_requests_from_AC_mode(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 50,
            "mode": 2,
            "spacetemp": 69
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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
        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 72
        }
        received_data = requests.get(lightsUrl + '/lastPUTMessage/4').json()
        self.assertEqual(received_data, expected_indoor_light_request)

        received_data = requests.get(lightsUrl + '/lastPUTMessage/2').json()
        self.assertEqual(received_data, expected_plant_light_request)

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

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
        self.assertNoInteractionsWithThermostat()

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
        self.assertNoInteractionsWithThermostat()

    def test_temp_down_command_with_AC_on_and_temp_more_than_2_above_min(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 2,
            "spacetemp": 70
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": 68
        }
        self.assertEqual(response.json(), expected_response)

        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 68
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_down_command_with_AC_on_and_temp_more_than_2_above_min_rounds_decimal_to_int(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 2,
            "spacetemp": 69.5
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": 68
        }
        self.assertEqual(response.json(), expected_response)

        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 68
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_down_command_with_AC_on_and_temp_more_than_2_above_min_rounds_decimal_to_int_and_handles_float_weirdness_well(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 2,
            "spacetemp": 70.5  # a magic number that makes python round wrong (at least on my laptop)
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": 69
        }
        self.assertEqual(response.json(), expected_response)

        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 69
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_down_command_with_AC_on_and_temp_less_than_2_above_min(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 2,
            "spacetemp": 67.5
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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

        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 67
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_down_command_with_AC_on_and_temp_already_at_min(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 2,
            "spacetemp": 67
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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

        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 67
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_down_command_with_AC_on_and_temp_less_than_min(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 2,
            "spacetemp": 65
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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

        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 67
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_down_command_with_Furnace_on(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 1,
            "spacetemp": 65
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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

        expected_thermostat_request = {
            'mode': 1,
            'heattemp': 63,
            'cooltemp': 70
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_down_command_with_Furnace_on_rounds_setting(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 1,
            "spacetemp": 68.5
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-down'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "furnace",
            "target-temp": 67
        }
        self.assertEqual(response.json(), expected_response)

        expected_thermostat_request = {
            'mode': 1,
            'heattemp': 67,
            'cooltemp': 70
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_up_command_with_Furnace_on_and_temp_more_than_2_below_max(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 1,
            "spacetemp": 66
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-up'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-up",
            "result": "success",
            "temperature-mode": "furnace",
            "target-temp": 68
        }
        self.assertEqual(response.json(), expected_response)

        expected_thermostat_request = {
            'mode': 1,
            'heattemp': 68,
            'cooltemp': 70
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_up_command_with_Furnace_on_and_temp_more_than_2_below_max_rounds_DOWN(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 1,
            "spacetemp": 65.5
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-up'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-up",
            "result": "success",
            "temperature-mode": "furnace",
            "target-temp": 67
        }
        self.assertEqual(response.json(), expected_response)

        expected_thermostat_request = {
            'mode': 1,
            'heattemp': 67,
            'cooltemp': 70
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_up_command_with_furnace_on_and_temp_less_than_2_below_max(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 1,
            "spacetemp": 71
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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

        expected_thermostat_request = {
            'mode': 1,
            'heattemp': 72,
            'cooltemp': 70
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_up_command_with_furnace_on_and_temp_already_at_max(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 1,
            "spacetemp": 72
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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

        expected_thermostat_request = {
            'mode': 1,
            'heattemp': 72,
            'cooltemp': 70
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_up_command_with_furnace_on_and_temp_above_max(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 1,
            "spacetemp": 92
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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

        expected_thermostat_request = {
            'mode': 1,
            'heattemp': 72,
            'cooltemp': 70
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)

    def test_temp_up_command_with_AC_on(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 2,
            "spacetemp": 65
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

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

        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 67
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)


    def test_temp_up_command_with_AC_on_rounds_down(self):
        current_thermostat_readings = {
            "heattemp": 80,
            "cooltemp": 70,
            "mode": 2,
            "spacetemp": 66.5
        }
        requests.post(thermostatUrl + "/query/info/set-mock", json=current_thermostat_readings)

        request_json = {'command': 'house-temp-up'}
        response = requests.put(self.get_server_url() + '/house/command', json=request_json, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "command": "house-temp-up",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": 68
        }
        self.assertEqual(response.json(), expected_response)

        expected_thermostat_request = {
            'mode': 2,
            'heattemp': 80,
            'cooltemp': 68
        }

        received_data = requests.get(thermostatUrl + '/lastThermostatStatePostRequest').json()
        self.assertEqual(received_data, expected_thermostat_request)
