#!env/bin/python

import unittest
import requests
from app import app
from flask.ext.testing import LiveServerTestCase

class SendMessageIntegrationTestCase(LiveServerTestCase):
    
    def create_app(self):
        testApp = app
        testApp.config['TESTING'] = True
        testApp.config['LIVESERVER_PORT'] = 8945
        testApp.config['MY_HOUSE_URL'] = 'http://127.0.0.1:3333'
        return testApp
    
    def test_mock_service_is_up(self):
        response = requests.get(app.config.get('MY_HOUSE_URL'))
        self.assertEqual(response.status_code, 200)