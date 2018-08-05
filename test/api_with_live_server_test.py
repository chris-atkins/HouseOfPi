#!env/bin/python

from test_server_setup import buildTestServer
from flask_testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport

class MyTestCase(LiveServerTestCase):
    
    def create_app(self):
        return buildTestServer()
        
    def test_client_directly(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hi there!')
