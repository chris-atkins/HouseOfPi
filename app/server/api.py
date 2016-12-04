#!env/bin/python
from flask import request, send_from_directory, jsonify  # @UnresolvedImport
import requests  # @UnresolvedImport
import os
from app.server.utils.endpoints import listEndpoints

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
    def  winkEndpoint():
        app.hardware.blink_n_times_in_time(number_of_blinks=20, seconds_to_blink=2)
        return ';)'
    
    @app.route('/textMe', methods=['GET'])
    def textMe():
        #     http://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python
        url = app.config.get('MY_HOUSE_URL') + '/house/notification'
        postData = {"messageContent": "Raspberry Pi says hi and would like to inform you that it was asked to send you a message."}
        
        response = requests.post(url, json=postData, verify=False)
        return response.json()['message']

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
#         print(app.root_path)  - this has been a problem in the past - print this in some other endpoint - this doesn't print here if the file is not found
        return send_from_directory(os.path.join(app.root_path, 'app/server/static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/tstat', methods=['GET'])
    def get_thermostat_state():
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        response = requests.get(url)
        return jsonify(response.json())

    @app.route('/tstat', methods=['POST'])
    def set_thermostat_state():
        url = app.config.get('THERMOSTAT_URL') + '/tstat'
        response = requests.post(url, json=request.get_json(force=True))
        return jsonify(response.json())