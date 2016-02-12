#!env/bin/python
from app import app   # @UnresolvedImport
from flask import request  # @UnresolvedImport
import requests  # @UnresolvedImport
import os
from flask import send_from_directory  # @UnresolvedImport

hiName = ''

@app.route('/')
def hello_world():
    return 'Hi there!'

@app.route('/hi', methods=['POST'])
def hiEndpoint():
    global hiName
    hiName = request.json.get('name')
    return 'ok'
    
@app.route('/hi', methods=['GET'])
def getHi():
    print 'hiName: ' + hiName
    return 'Hi ' + hiName

@app.route('/textMe', methods=['GET'])
def textMe():
    #     http://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python
    url = app.config.get('MY_HOUSE_URL') + '/house/notification'
    postData = {"messageContent": "Raspberry Pi says hi and would like to inform you that it was asked to send you a message."}
    
    response = requests.post(url, json=postData, verify=False)
    return response.json()['message']

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
