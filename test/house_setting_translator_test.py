import unittest

from app.server.house_setting_translator import HouseSettingTranslator


class HouseSettingTranslatorTest(unittest.TestCase):

    def test_ac_mode_fan_on(self):
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
            "temp_setting": 68.5,
            "current_temp": 63,
            "fan_on": True
        }
        self.assertEqual(result, expected)


    def test_furnace_mode_fan_on(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 1,
            "t_heat": 70.5,
            "tstate": 1,
            "fstate": 1
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        expected = {
            "mode": "FURNACE",
            "temp_setting": 70.5,
            "current_temp": 69.5,
            "fan_on": True
        }
        self.assertEqual(result, expected)

    def test_ac_mode_fan_off(self):
        thermostat_json = {
            "temp": 63,
            "tmode": 2,
            "t_cool": 68.5,
            "tstate": 2,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        expected = {
            "mode": "AC",
            "temp_setting": 68.5,
            "current_temp": 63,
            "fan_on": False
        }
        self.assertEqual(result, expected)

    def test_furnace_mode_fan_off(self):
        thermostat_json = {
            "temp": 69.5,
            "tmode": 1,
            "t_heat": 70.5,
            "tstate": 1,
            "fstate": 0
        }
        result = HouseSettingTranslator().translate(thermostat_json)

        expected = {
            "mode": "FURNACE",
            "temp_setting": 70.5,
            "current_temp": 69.5,
            "fan_on": False
        }
        self.assertEqual(result, expected)

