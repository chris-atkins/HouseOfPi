#!env/bin/python

import requests
from app import app
from flask.ext.testing import LiveServerTestCase

class TextMeIntegrationTestCase(LiveServerTestCase):
    
    global myHouseUrl
    myHouseUrl = 'http://127.0.0.1:3333'
    
    def create_app(self):
        testApp = app
        testApp.config['TESTING'] = True
        testApp.config['LIVESERVER_PORT'] = 8945
        testApp.config['MY_HOUSE_URL'] = myHouseUrl
        return testApp
    
    def test_mock_service_is_up(self):
        response = requests.get(myHouseUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Server is up')
        
    def test_text_me_calls_mock(self):
        requests.get(self.get_server_url() + '/textMe')
        sentToMyHouseResponse = requests.get(myHouseUrl + '/notifyWasCalled')
        self.assertEquals(sentToMyHouseResponse.text, 'True')
        
    def test_text_me_returns_message_from_remote_server(self):
        response = requests.get(self.get_server_url() + '/textMe')
        self.assertEquals(response.text, 'Notify stub response')