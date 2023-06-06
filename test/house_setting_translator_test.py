import unittest

from app.server.house_status_translator import HouseStatusTranslator


class HouseSettingTranslatorTest(unittest.TestCase):

    def test_whole_response(self):
        thermostat_json = {
            "name": "THERMOSTAT",
            "mode": 2,
            "state": 2,
            "activestage": 0,
            "fan": 0,
            "fanstate": 1,
            "tempunits": 0,
            "schedule": 0,
            "schedulepart": 0,
            "away": 0,
            "spacetemp": 63.0,
            "heattemp": 62.0,
            "cooltemp": 68.5,
            "cooltempmin": 35.0,
            "cooltempmax": 99.0,
            "heattempmin": 35.0,
            "heattempmax": 99.0,
            "setpointdelta": 2,
            "availablemodes": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        expected = {
            "mode": "AC",
            "current_temp": 63,
            "temp_setting": 68.5,
            "state": "AC_ON",
            "fan_on": True
        }
        self.assertEqual(result, expected)


    def test_fan_on(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 70.5,
            "state": 1,
            "fanstate": 1
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["fan_on"], True)

    def test_ac_mode_fan_off(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 2,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["fan_on"], False)

    def test_thermostat_mode_off(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 0,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["mode"], "OFF")

    def test_thermostat_mode_furnace(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["mode"], "FURNACE")

    def test_thermostat_mode_AC(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 2,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["mode"], "AC")

    def test_thermostat_mode_auto(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 3,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["mode"], "AUTO")

    def test_furnace_state_off(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["state"], "OFF")

    def test_furnace_state_heat(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 70.5,
            "state": 1,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["state"], "HEAT_ON")

    def test_furnace_state_cool(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 70.5,
            "state": 2,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["state"], "AC_ON")

    def test_furnace_state_lockout(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 70.5,
            "state": 3,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["state"], "LOCKOUT")

    def test_furnace_state_error(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 70.5,
            "state": 4,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["state"], "ERROR")

    def test_current_temp_decimal(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 69.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["current_temp"], 69.5)

    def test_current_temp_int(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 69,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["current_temp"], 69)

    def test_target_temp_heat(self):
        thermostat_json = {
            "heattemp": 70.3,
            "cooltemp": 88,
            "mode": 1,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["temp_setting"], 70.3)

    def test_target_temp_cool(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 2,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["temp_setting"], 88)

    def test_target_temp_auto_returns_cooltemp(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 3,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["temp_setting"], 88)

    def test_target_temp_off_returns_cooltemp(self):
        thermostat_json = {
            "heattemp": 69.5,
            "cooltemp": 88,
            "mode": 0,
            "spacetemp": 70.5,
            "state": 0,
            "fanstate": 0
        }
        result = HouseStatusTranslator().translate(thermostat_json)

        self.assertEqual(result["temp_setting"], 88)

