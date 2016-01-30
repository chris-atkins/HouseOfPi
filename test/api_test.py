#!env/bin/python

import unittest
from app import app

class MyTestCase(unittest.TestCase):
    
    def setup_class(self):
        self.app = app.test_client();
        
    def test_client_directly(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.data, 'Hi there!')