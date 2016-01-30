#!env/bin/python

from app import app
from flask import Flask
from flask.ext.testing import LiveServerTestCase
import requests


class MyTestCase(LiveServerTestCase):
    
    def create_app(self):
        testApp = app
        testApp.config['TESTING'] = True
        testApp.config['LIVESERVER_PORT'] = 8945
        return testApp
        
    def test_client_directly(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hi there!')