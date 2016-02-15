#!env/bin/python

import unittest
from test_server_setup import buildTestServer

class MyTestCase(unittest.TestCase):
    
    def setup_class(self):
        self.app = buildTestServer().test_client();
        
    def test_client_directly(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.data, b'Hi there!')