#!env/bin/python
from app.hardware.house_of_pi import HouseOfPi
import unittest
from mock import MagicMock
from mock import call
from mock import patch

class HouseOfPiTest(unittest.TestCase):

    def setUp(self):
        self.mock_gpio_factory = MagicMock()
        self.mock_gpio = self.mock_gpio_factory.getGPIO.return_value
    
    
    def test_GPIO_setup_in_board_config(self):
        HouseOfPi(self.mock_gpio_factory)
        self.mock_gpio.setmode.assert_called_once_with(self.mock_gpio.BOARD)
        
    
    def test_green_LED_setup(self):
        pi = HouseOfPi(self.mock_gpio_factory)
        self.assertEquals(pi.GREEN_LED, 11)
        
        expected_args = call(pi.GREEN_LED, self.mock_gpio.OUT)
        self.assertTrue(expected_args in self.mock_gpio.setup.call_args_list)
        
    
    def test_blue_LED_setup(self):
        pi = HouseOfPi(self.mock_gpio_factory)
        self.assertEquals(pi.BLUE_LED, 13)
        
        expected_args = call(pi.BLUE_LED, self.mock_gpio.OUT)
        self.assertTrue(expected_args in self.mock_gpio.setup.call_args_list)
    
    
    @patch('app.hardware.house_of_pi.TimedLEDDisplay')
    def test_start_displaying_on_state_is_wired_correctly(self, mock_LED_display):
        mock_LED_display_instance = mock_LED_display.return_value
        pi = HouseOfPi(self.mock_gpio_factory)
        pi.start_displaying_on_state(42)
        
        mock_LED_display.assert_called_with(self.mock_gpio, 42)
        mock_LED_display_instance.start_led_display_every.assert_called_with(pi.led_display_cycle_time)
    
    
    @patch('app.hardware.house_of_pi.WinkDisplay')
    def test_wink_display_is_wired_correctly(self, mock_winker):
        mock_winker_instance = mock_winker.return_value
        pi = HouseOfPi(self.mock_gpio_factory)
        channel = 33
        number_of_blinks = 23
        seconds_to_blink = 48
        
        pi.blink_n_times_in_time(channel = channel, number_of_blinks = number_of_blinks, seconds_to_blink = seconds_to_blink)
        
        mock_winker.assert_called_with(self.mock_gpio, channel)
        mock_winker_instance.wink.assert_called_with(number_of_blinks, seconds_to_blink)


    def test_on_called_one_time(self):
        pi = HouseOfPi(self.mock_gpio_factory)
        pi.blink_n_times_in_time(13, 1, 1)
        self.assertTrue(self.mock_gpio.output.called)
    
