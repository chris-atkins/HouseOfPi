#!flask/bin/python
from app import app # @UnresolvedImport

hiName = ''

@app.route('/')
def hello_world():
    return 'Hi theres!'

@app.route('/hi', methods=['POST'])
def hiEndpoint():
    return 'ok'
    
@app.route('/hi', methods=['GET'])
def getHi():
    return 'Hi ' + hiName
