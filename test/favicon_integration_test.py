#!env/bin/python

import requests  # @UnresolvedImport
from app.server import app  # @UnresolvedImport
from flask.ext.testing import LiveServerTestCase  # @UnresolvedImport

class TextMeIntegrationTestCase(LiveServerTestCase):
    
    global myHouseUrl
    myHouseUrl = 'http://127.0.0.1:3333'
    
    def create_app(self):
        testApp = app
        testApp.config['TESTING'] = True
        testApp.config['LIVESERVER_PORT'] = 8945
        testApp.config['MY_HOUSE_URL'] = myHouseUrl
        return testApp

    def test_favicon_works(self):
        response = requests.get(self.get_server_url() + '/favicon.ico')
        self.assertIsNotNone(response.content);
        self.assertGreater(len(response.content), 255)
        