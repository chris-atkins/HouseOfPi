#!env/bin/python

from app import app
from flask import Flask
from flask.ext.testing import LiveServerTestCase
import requests
import threading


class MyTestCase(LiveServerTestCase):
    
    def create_app(self):
        testApp = app
        testApp.config['TESTING'] = True
        testApp.config['LIVESERVER_PORT'] = 8945
        testApp.config['MY_HOUSE_URL'] = 'http://127.0.0.1:3333'
            
#         t = threading.Thread(target=mock_my_house_server.app.run, kwargs={'host':'127.0.0.1', 'port':3333})
#         t.daemon = True
#         t.start()    
        
        return testApp
        
    def test_client_directly(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hi there!')
