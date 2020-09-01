#!env/bin/python


class HouseSettingTranslator(object):

    def translate(self, thermostat_json):
        mode = self.translate_mode(thermostat_json["tmode"])
        temp_setting_key = self.get_key_for_mode(mode)
        temp_setting = thermostat_json[temp_setting_key]
        current_temp = thermostat_json["temp"]
        fan_on = self.translate_fan_on(thermostat_json["fstate"])

        return {
            "mode": mode,
            "temp_setting": temp_setting,
            "current_temp": current_temp,
            "fan_on": fan_on
        }

    def translate_mode(self, value):
        if value is 2:
            return "AC"
        if value is 1:
            return "FURNACE"
        return "UNKNOWN"

    def get_key_for_mode(self, mode):
        if mode is "AC":
            return "t_cool"
        if mode is "FURNACE":
            return "t_heat"
        return "UNKNOWN"

    def translate_fan_on(self, value):
        if value is 0:
            return False
        if value is 1:
            return True
        return "UNKNOWN"
