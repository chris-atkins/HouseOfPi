#!env/bin/python
from app.hardware.house_of_pi import HouseOfPi
import unittest
from mock import MagicMock
import time

class HouseOfPiTest(unittest.TestCase):

    def test_on_called_one_time(self):
        mock_gpio_factory = MagicMock()
        mock_gpio = MagicMock()
        mock_gpio_factory.getGPIO.return_value = mock_gpio
        
        pi = HouseOfPi(mock_gpio_factory)
        pi.blink_n_times_in_time(1, 1)
        self.assertTrue(mock_gpio.output.called)
    
