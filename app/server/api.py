#!env/bin/python
from flask import request, send_from_directory, jsonify, Response
import requests
import os
from app.server.authentication_interceptor import authenticate
from app.server.house_command_request_creator import create_requests_for_mode
from app.server.house_status_translator import HouseStatusTranslator


def initRoutes(app):
    
    hiName = ''

    @app.route('/')
    def hello_world():
        print(app.root_path)
        return 'Hi there!'
    
    @app.route('/hi', methods=['POST'])
    def hiEndpoint():
        global hiName
        hiName = request.json.get('name')
        return 'ok' 
        
    @app.route('/hi', methods=['GET'])
    def getHi():
        print('hiName: ' + hiName)
        return 'Hi ' + hiName
    
    @app.route('/endpoints', methods=['GET'])
    def listEndpoints():
        return str(listEndpoints(app))
    
    @app.route('/wink', methods=['GET'])
    @authenticate(configuration=app.config)
    def winkEndpoint():
        app.hardware.blink_n_times_in_time(number_of_blinks=20, seconds_to_blink=2)
        return ';)'
    
    @app.route('/textMe', methods=['GET'])
    @authenticate(configuration=app.config)
    def textMe():
        #     http://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python
        url = app.config.get('MY_HOUSE_URL') + '/house/notification'
        postData = {"messageContent": "Raspberry Pi says hi and would like to inform you that it was asked to send you a message."}
        
        response = requests.post(url, json=postData, verify=False)
        return response.json()['message']

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        # print(app.root_path)  - this has been a problem in the past - print this in some other endpoint - this doesn't print here if the file is not found
        return send_from_directory(os.path.join(app.root_path, 'app/server/static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/house/status', methods=['GET'])
    @authenticate(configuration=app.config)
    def get_house_status():
        url = app.config.get('THERMOSTAT_URL') + '/query/info'
        thermostat_response = requests.get(url)
        house_status = HouseStatusTranslator().translate(thermostat_response.json())
        return jsonify(house_status)

    @app.route('/thermostat/state', methods=['POST'])
    @authenticate(configuration=app.config)
    def set_house_temp():
        # request = {
        #     targetTemp: 34,
        #     mode: CURRENT || HEAT || COOL
        # }

        requested_mode = request.get_json()['mode']
        requested_temp = request.get_json()['targetTemp']

        thermostat_response = requests.get(app.config.get('THERMOSTAT_URL') + '/query/info')
        current_status = thermostat_response.json()

        new_heat = current_status['heattemp']
        new_cool = current_status['cooltemp']
        new_mode = current_status['mode']

        if requested_mode == 'HEAT' or (requested_mode == 'CURRENT' and new_mode == 1):
            new_heat = requested_temp
        if requested_mode == 'COOL' or (requested_mode == 'CURRENT' and new_mode == 2):
            new_cool = requested_temp

        if requested_mode == 'HEAT':
            new_mode = 1
        if requested_mode == 'COOL':
            new_mode = 2

        params = {
            'mode': new_mode,
            'heattemp': new_heat,
            'cooltemp': new_cool
        }
        url = app.config.get('THERMOSTAT_URL') + '/control'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=params, headers=headers)
        return Response(status=response.status_code)

    @app.route('/lights/state', methods=['PUT'])
    @authenticate(configuration=app.config)
    def set_lights_state():
        url = app.config.get('LIGHTS_URL') + '/api/6b1abf1f6e7157cc3843ee8b668d32d/groups/0/action'
        response = requests.put(url, json=request.get_json(force=True))
        return jsonify(response.json())

    @app.route('/house/command', methods=['PUT'])
    @authenticate(configuration=app.config)
    def set_house():
        mode = request.get_json()['command']

        thermostat_response = requests.get(app.config.get('THERMOSTAT_URL') + '/query/info')
        thermostat_status = thermostat_response.json()

        if mode == "house-temp-down":
            return handle_house_temp_down(thermostat_status)
        if mode == "house-temp-up":
            return handle_house_temp_up(thermostat_status)
        if mode == "at-work-mode":
            mode = translate_at_work_mode(thermostat_status)

        #TODO
        # if mode == "night-time"
        #     return dostuff()
        # if mode == "morning"
        #     return dostuff()

        house_requests = create_requests_for_mode(mode=mode, app_config=app.config, thermostat_status=thermostat_status)

        for house_request in house_requests:
            if house_request.request_type == 'put':
                requests.put(house_request.url, json=house_request.body)
            elif house_request.request_type == 'post':
                requests.post(house_request.url, json=house_request.body)
            elif house_request.request_type == 'form':
                requests.post(house_request.url, data=house_request.body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            elif house_request.request_type == 'wemo':
                for wemo in app.wemoDevices:
                    wemo.set_brightness(house_request.body)

        return jsonify({'status': 'success'})

    def handle_house_temp_down(thermostat_status):
        house_mode = thermostat_status["mode"]

        if house_mode == 2:
            return handle_temp_down_with_ac_on(thermostat_status)
        else:
            return handle_temp_down_with_furnace_on(thermostat_status)

    def handle_temp_down_with_ac_on(thermostat_status):
        house_temp = thermostat_status["spacetemp"]
        result = "success"
        if house_temp <= 67:
            result = "no-change"

        temp_to_set = round(house_temp + .0005 - 2)  # because the thermostat does this rounding itself, and we don't want to lie in our response - so if we round first, we control the behavior
        if temp_to_set < 67:
            temp_to_set = 67

        heat_request = {
            'cooltemp': temp_to_set,
            'mode': 2,
            'heattemp': thermostat_status['heattemp']
        }
        url = app.config.get('THERMOSTAT_URL') + '/control'
        requests.post(url, data=heat_request, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        response = {
            "command": "house-temp-down",
            "result": result,
            "temperature-mode": "AC",
            "target-temp": temp_to_set
        }
        return jsonify(response)

    def handle_temp_down_with_furnace_on(thermostat_status):
        house_temp = thermostat_status["spacetemp"]
        temp_to_set = round(house_temp + .0005 - 2)  # the adding .0005 is to deal with weirdness in float numbers
        heat_request = {
            'cooltemp': thermostat_status['cooltemp'],
            'mode': 1,
            'heattemp': temp_to_set
        }
        url = app.config.get('THERMOSTAT_URL') + '/control'
        requests.post(url, data=heat_request, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "furnace",
            "target-temp": temp_to_set
        }
        return jsonify(response)

    def handle_house_temp_up(thermostat_status):
        house_mode = thermostat_status["mode"]
        house_temp = thermostat_status["spacetemp"]

        if house_mode == 1:
            return handle_temp_up_with_furnace_on(thermostat_status)
        else:
            return handle_temp_up_with_ac_on(thermostat_status)

    def handle_temp_up_with_furnace_on(thermostat_status):
        house_temp = thermostat_status["spacetemp"]
        result = "success"
        if house_temp >= 72:
            result = "no-change"

        temp_to_set = round(house_temp - .0005 + 2) # round down so we only do a 1.5 increment, not 2.5
        if temp_to_set > 72:
            temp_to_set = 72

        heat_request = {
            'cooltemp': thermostat_status['cooltemp'],
            'mode': 1,
            'heattemp': temp_to_set
        }
        url = app.config.get('THERMOSTAT_URL') + '/control'
        requests.post(url, data=heat_request, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        response = {
            "command": "house-temp-up",
            "result": result,
            "temperature-mode": "furnace",
            "target-temp": temp_to_set
        }
        return jsonify(response)

    def handle_temp_up_with_ac_on(thermostat_status):
        house_temp = thermostat_status["spacetemp"]
        temp_to_set = round(house_temp - .0005 + 2)
        heat_request = {
            'cooltemp': temp_to_set,
            'mode': 2,
            'heattemp': thermostat_status['heattemp']
        }
        url = app.config.get('THERMOSTAT_URL') + '/control'
        requests.post(url, data=heat_request, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        response = {
            "command": "house-temp-up",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": temp_to_set
        }
        return jsonify(response)

    def translate_at_work_mode(thermostat_status):
        house_mode = thermostat_status['mode']
        if house_mode == 1:
            return "at-work-mode-furnace"
        else:
            return "at-work-mode-ac"

