
class HouseRequest:
    def __init__(self, url, body):
        self.url = url
        self.body = body


def create_requests_for_mode(mode, app_config):

    if mode == 'lights-on':
        url = app_config.get('LIGHTS_URL') + group_path(group='0')
        body = build_light_request_body(on=True)
        request = HouseRequest(url, body)
        return [request]

    elif mode == 'lights-off':
        url = app_config.get('LIGHTS_URL') + group_path(group='0')
        body = build_light_request_body(on=False)
        request = HouseRequest(url, body)
        return [request]

    elif mode == 'at-work':
        plant_light_url = app_config.get('LIGHTS_URL') + group_path(group='2')
        plant_light_body = build_light_request_body(on=True)
        plant_light_request = HouseRequest(plant_light_url, plant_light_body)

        other_lights_url = app_config.get('LIGHTS_URL') + group_path(group='1')
        other_lights_body = build_light_request_body(on=False)
        other_lights_request = HouseRequest(other_lights_url, other_lights_body)

        return [other_lights_request, plant_light_request]


def group_path(group):
    return '/api/6b1abf1f6e7157cc3843ee8b668d32d/groups/' + group + '/action'


def build_light_request_body(on):
    return {
        'on': on,
        'bri': 254,
        'hue': 19228,
        'sat': 13,
        'ct': 257,
        'effect': 'none',
        'alert': 'none',
        'xy': [0.3852, 0.3815]
    }