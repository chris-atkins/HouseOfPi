#!flask/bin/python

import unittest
from app import api

def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)

    def test_api_hello_world(self):
        response = api.hello_world()
        self.assertEqual(response, "Hi there!")