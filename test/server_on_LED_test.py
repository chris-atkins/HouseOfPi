#!env/bin/python

from test_server_setup import buildTestServer
from flask.ext.testing import LiveServerTestCase  # @UnresolvedImport
import pickle
import time

class ServerOnLEDTest(LiveServerTestCase):
    
    def create_app(self):
        return buildTestServer(track_gpio_calls = True)

    def test_setup_called_on_correct_pin(self):
        gpio = self.load_tracked_gpio()
        self.assertTrue(gpio.setup_was_called_for_channel(11))
    
    def test_on_and_off_called_every_2_seconds(self):
        time.sleep(4)
        gpio = self.load_tracked_gpio()
        print(gpio.number_of_high_calls_for_channel(11))
        print(gpio.number_of_low_calls_for_channel(11))
        self.assertTrue(gpio.number_of_high_calls_for_channel(11) >= 2)
        self.assertTrue(gpio.number_of_low_calls_for_channel(11) >= 2)
    
    def load_tracked_gpio(self):
        with open('gpio.pickle', 'rb') as f:
            return pickle.load(f)    
    