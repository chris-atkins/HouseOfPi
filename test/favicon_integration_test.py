#!env/bin/python

from test_server_setup import buildTestServer
from flask_testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport

class TextMeIntegrationTestCase(LiveServerTestCase):
    
    def create_app(self):
        return buildTestServer()

    def test_favicon_works(self):
        response = requests.get(self.get_server_url() + '/favicon.ico')
        self.assertIsNotNone(response.content);
        self.assertGreater(len(response.content), 255)
