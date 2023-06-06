#!env/bin/python


class HouseStatusTranslator(object):

    def translate(self, thermostat_json):
        mode = self.translate_mode(thermostat_json["mode"])
        temp_setting = self.find_temp_setting(thermostat_json)
        current_temp = thermostat_json["spacetemp"]
        fan_on = self.translate_fan_on(thermostat_json["fanstate"])
        state = self.translate_state(thermostat_json["state"])

        return {
            "mode": mode,
            "current_temp": current_temp,
            "temp_setting": temp_setting,
            "state": state,
            "fan_on": fan_on
        }

    def find_temp_setting(self, thermostat_json):
        mode = self.translate_mode(thermostat_json["mode"])
        if mode == "FURNACE":
            return thermostat_json["heattemp"]

        return thermostat_json["cooltemp"]

    def translate_mode(self, value):
        if value == 0:
            return "OFF"
        if value == 1:
            return "FURNACE"
        if value == 2:
            return "AC"
        if value == 3:
            return "AUTO"
        return "UNKNOWN"

    def translate_fan_on(self, value):
        if value == 0:
            return False
        if value == 1:
            return True
        return "UNKNOWN"

    def translate_state(self, value):
        if value == 0:
            return "OFF"
        if value == 1:
            return "HEAT_ON"
        if value == 2:
            return "AC_ON"
        if value == 3:
            return "LOCKOUT"
        if value == 4:
            return "ERROR"
        return "UNKNOWN"
