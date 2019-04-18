
class HouseRequest:
    def __init__(self, url, body, request_type):
        self.url = url
        self.body = body
        self.request_type = request_type


def create_requests_for_mode(mode, app_config):

    if mode == 'lights-on':
        url = app_config.get('LIGHTS_URL') + group_path(group='4')
        body = build_light_request_body(on=True)
        request = HouseRequest(url, body, 'put')
        return [request]

    elif mode == 'dim-lights':
        url = app_config.get('LIGHTS_URL') + group_path(group='4')
        body = build_light_request_body(on=True, brightness=73)
        request = HouseRequest(url, body, 'put')
        return [request]

    elif mode == 'lights-off':
        url = app_config.get('LIGHTS_URL') + group_path(group='4')
        body = build_light_request_body(on=False)
        request = HouseRequest(url, body, 'put')
        return [request]

    if mode == 'outside-lights-on':
        url = app_config.get('LIGHTS_URL') + group_path(group='3')
        body = build_light_request_body(on=True)
        request = HouseRequest(url, body, 'put')
        return [request]

    elif mode == 'outside-lights-off':
        url = app_config.get('LIGHTS_URL') + group_path(group='3')
        body = build_light_request_body(on=False)
        request = HouseRequest(url, body, 'put')
        return [request]

    elif mode == 'at-work-mode':
        plant_light_url = app_config.get('LIGHTS_URL') + group_path(group='2')
        plant_light_body = build_light_request_body(on=True)
        plant_light_request = HouseRequest(plant_light_url, plant_light_body, 'put')

        other_lights_url = app_config.get('LIGHTS_URL') + group_path(group='1')
        other_lights_body = build_light_request_body(on=False)
        other_lights_request = HouseRequest(other_lights_url, other_lights_body, 'put')

        temperature_url = app_config.get('THERMOSTAT_URL') + '/tstat'
        temperature_body = {'t_heat':64.0,'tmode':1,'hold':1}
        temperature_request = HouseRequest(temperature_url, temperature_body, 'post')

        return [other_lights_request, plant_light_request, temperature_request]


def group_path(group):
    return '/api/6b1abf1f6e7157cc3843ee8b668d32d/groups/' + group + '/action'


def build_light_request_body(on,brightness=254):
    return {
        'on': on,
        'bri': brightness,
        'hue': 19228,
        'sat': 13,
        'ct': 257,
        'effect': 'none',
        'alert': 'none',
        'xy': [0.3852, 0.3815]
    }