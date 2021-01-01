#!env/bin/python
from flask import request, send_from_directory, jsonify
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

    @app.route('/tstat', methods=['GET'])
    @authenticate(configuration=app.config)
    def get_thermostat_state():
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        response = requests.get(url)
        return jsonify(response.json())

    @app.route('/tstat', methods=['POST'])
    @authenticate(configuration=app.config)
    def set_thermostat_state():
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        response = requests.post(url, json=request.get_json(force=True))
        return jsonify(response.json())

    @app.route('/house/status', methods=['GET'])
    @authenticate(configuration=app.config)
    def get_house_status():
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        thermostat_response = requests.get(url)
        house_status = HouseStatusTranslator().translate(thermostat_response.json())
        return jsonify(house_status)

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

        if mode == "house-temp-down":
            return handle_house_temp_down()
        if mode == "house-temp-up":
            return handle_house_temp_up()
        if mode == "at-work-mode":
            mode = translate_at_work_mode()

        house_requests = create_requests_for_mode(mode=mode, app_config=app.config)

        for house_request in house_requests:
            if house_request.request_type == 'put':
                requests.put(house_request.url, json=house_request.body)
            elif house_request.request_type == 'post':
                requests.post(house_request.url, json=house_request.body)

        return jsonify({'status': 'success'})

    def handle_house_temp_down():
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        current_thermostat_settings = requests.get(url).json()

        house_mode = current_thermostat_settings["tmode"]
        house_temp = current_thermostat_settings["temp"]

        if house_mode is 2:
            return handle_temp_down_with_ac_on(house_temp)
        else:
            return handle_temp_down_with_furnace_on(house_temp)

    def handle_temp_down_with_ac_on(house_temp):
        result = "success"
        if house_temp <= 67:
            result = "no-change"

        temp_to_set = house_temp - 2
        if temp_to_set < 67:
            temp_to_set = 67

        heat_request = {
            't_cool': temp_to_set,
            'tmode': 2,
            'hold': 1
        }
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        requests.post(url, json=heat_request)

        response = {
            "command": "house-temp-down",
            "result": result,
            "temperature-mode": "AC",
            "target-temp": temp_to_set
        }
        return jsonify(response)

    def handle_temp_down_with_furnace_on(house_temp):
        temp_to_set = house_temp - 2
        heat_request = {
            't_heat': temp_to_set,
            'tmode': 1,
            'hold': 1
        }
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        requests.post(url, json=heat_request)

        response = {
            "command": "house-temp-down",
            "result": "success",
            "temperature-mode": "furnace",
            "target-temp": temp_to_set
        }
        return jsonify(response)

    def handle_house_temp_up():
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        current_thermostat_settings = requests.get(url).json()

        house_mode = current_thermostat_settings["tmode"]
        house_temp = current_thermostat_settings["temp"]

        if house_mode is 1:
            return handle_temp_up_with_furnace_on(house_temp)
        else:
            return handle_temp_up_with_ac_on(house_temp)

    def handle_temp_up_with_furnace_on(house_temp):
        result = "success"
        if house_temp >= 72:
            result = "no-change"

        temp_to_set = house_temp + 2
        if temp_to_set > 72:
            temp_to_set = 72

        heat_request = {
            't_heat': temp_to_set,
            'tmode': 1,
            'hold': 1
        }
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        requests.post(url, json=heat_request)

        response = {
            "command": "house-temp-up",
            "result": result,
            "temperature-mode": "furnace",
            "target-temp": temp_to_set
        }
        return jsonify(response)

    def handle_temp_up_with_ac_on(house_temp):
        temp_to_set = house_temp + 2
        heat_request = {
            't_cool': temp_to_set,
            'tmode': 2,
            'hold': 1
        }
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        requests.post(url, json=heat_request)

        response = {
            "command": "house-temp-up",
            "result": "success",
            "temperature-mode": "AC",
            "target-temp": temp_to_set
        }
        return jsonify(response)

    def translate_at_work_mode():
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        current_thermostat_settings = requests.get(url).json()

        house_mode = current_thermostat_settings["tmode"]

        if house_mode is 1:
            return "at-work-mode-furnace"
        else:
            return "at-work-mode-ac"

