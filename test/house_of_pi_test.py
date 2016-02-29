#!env/bin/python
from app.hardware.house_of_pi import HouseOfPi
import unittest
from mock import MagicMock
from mock import patch

class HouseOfPiTest(unittest.TestCase):

    def setUp(self):
        self.mock_gpio_factory = MagicMock()
        self.mock_gpio = self.mock_gpio_factory.getGPIO.return_value
    
    
    @patch('app.hardware.house_of_pi.TimedLEDDisplay')
    def test_start_displaying_on_state_is_wired_correctly(self, mock_LED_display):
        mock_LED_display_instance = mock_LED_display.return_value
        pi = HouseOfPi(self.mock_gpio_factory)
        pi.start_displaying_on_state(42)
        
        mock_LED_display.assert_called_with(self.mock_gpio, 42)
        mock_LED_display_instance.start_led_display_every.assert_called_with(pi.led_display_cycle_time)


    def test_on_called_one_time(self):
        pi = HouseOfPi(self.mock_gpio_factory)
        pi.blink_n_times_in_time(1, 1)
        self.assertTrue(self.mock_gpio.output.called)
    
