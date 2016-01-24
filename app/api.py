from app import app

hiName = ''

@app.route('/')
def hello_world():
    return 'Hi there!'

@app.route('/hi', methods=['POST'])
def hiEndpoint():
    return 'ok'
    
@app.route('/hi', methods=['GET'])
def getHi():
    return 'Hi ' + hiName
