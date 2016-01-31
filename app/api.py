#!env/bin/python
from app import app 
from flask import request
import requests

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
    url = app.config.get('MY_HOUSE_URL') + '/house/notify'
    response = requests.get(url, verify=False)

    return response.text