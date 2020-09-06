#!env/bin/python


class HouseSettingTranslator(object):

    def translate(self, thermostat_json):
        mode = self.translate_mode(thermostat_json["tmode"])
        temp_setting = self.find_temp_setting(thermostat_json)
        current_temp = thermostat_json["temp"]
        fan_on = self.translate_fan_on(thermostat_json["fstate"])
        state = self.translate_state(thermostat_json["tstate"])

        return {
            "mode": mode,
            "current_temp": current_temp,
            "temp_setting": temp_setting,
            "state": state,
            "fan_on": fan_on
        }

    def find_temp_setting(self, thermostat_json):
        if "t_cool" in thermostat_json:
            return thermostat_json["t_cool"]
        if "t_heat" in thermostat_json:
            return thermostat_json["t_heat"]
        return "UNKNOWN"

    def translate_mode(self, value):
        if value is 0:
            return "OFF"
        if value is 1:
            return "FURNACE"
        if value is 2:
            return "AC"
        if value is 3:
            return "AUTO"
        return "UNKNOWN"

    def translate_fan_on(self, value):
        if value is 0:
            return False
        if value is 1:
            return True
        return "UNKNOWN"

    def translate_state(self, value):
        if value is 0:
            return "OFF"
        if value is 1:
            return "HEAT_ON"
        if value is 2:
            return "AC_ON"
        return "UNKNOWN"
