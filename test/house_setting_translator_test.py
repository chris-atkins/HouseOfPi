import unittest

from app.server.house_setting_translator import HouseSettingTranslator


class HouseSettingTranslatorTest(unittest.TestCase):

    def test_whole_response(self):
        thermostat_json = {
            "temp": 63,
            "tmode": 2,
            "t_cool": 68.5,
            "tstate": 2,
            "fstate": 1
        }
        result = HouseSettingTranslator().translate(thermostat_json)

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
            "temp": 69.5,
            "tmode": 1,
            "t_heat": 70.5,
            "tstate": 1,
            "fstate": 1
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["fan_on"], True)

    def test_ac_mode_fan_off(self):
        thermostat_json = {
            "temp": 63,
            "tmode": 2,
            "t_cool": 68.5,
            "tstate": 2,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["fan_on"], False)

    def test_thermostat_mode_off(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 0,
            "t_heat": 70.5,
            "tstate": 1,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["mode"], "OFF")

    def test_thermostat_mode_furnace(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 1,
            "t_heat": 70.5,
            "tstate": 1,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["mode"], "FURNACE")

    def test_thermostat_mode_AC(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 2,
            "t_heat": 70.5,
            "t_cool": 70.5,
            "tstate": 1,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["mode"], "AC")

    def test_thermostat_mode_auto(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 3,
            "t_heat": 70.5,
            "tstate": 1,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["mode"], "AUTO")

    def test_furnace_state_off(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 3,
            "t_heat": 70.5,
            "tstate": 0,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["state"], "OFF")

    def test_furnace_state_heat(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 3,
            "t_heat": 70.5,
            "tstate": 1,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["state"], "HEAT_ON")

    def test_furnace_state_cool(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 3,
            "t_heat": 70.5,
            "tstate": 2,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["state"], "AC_ON")

    def test_current_temp_decimal(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 3,
            "t_heat": 70.5,
            "tstate": 2,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["current_temp"], 69.5)

    def test_current_temp_int(self):
        thermostat_json = {
            "temp": 69,
            "tmode": 3,
            "t_heat": 70.5,
            "tstate": 2,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["current_temp"], 69)

    def test_target_temp_heat(self):
        thermostat_json = {
            "temp": 69,
            "tmode": 3,
            "t_heat": 70.3,
            "tstate": 2,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["temp_setting"], 70.3)

    def test_target_temp_ool(self):
        thermostat_json = {
            "temp": 69,
            "tmode": 3,
            "t_cool": 70.5,
            "tstate": 2,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        self.assertEqual(result["temp_setting"], 70.5)

