#!env/bin/python

from app.server import app  # @UnresolvedImport
from flask.ext.testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport
# import threading


class MyTestCase(LiveServerTestCase):
    
    def create_app(self):
        testApp = app
        testApp.config['TESTING'] = True
        testApp.config['LIVESERVER_PORT'] = 8945
        testApp.config['MY_HOUSE_URL'] = 'http://127.0.0.1:3333'
        
        return testApp
        
    def test_client_directly(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hi there!')
