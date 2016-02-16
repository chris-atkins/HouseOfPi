#!env/bin/python
from app.server.hardware_interface import HardwareInterface 
from app.hardware.app_status_display import TimedLEDDisplay

class HouseOfPi(HardwareInterface):

    def __init__(self, gpio_factory):
        super(HouseOfPi, self).__init__()
        self.GPIO = gpio_factory.getGPIO()
        self.led_display_cycle_time = 2
        
    def start_displaying_on_state(self, channel_in_board_scheme=11):
        ledDisplay = TimedLEDDisplay(self.GPIO, channel_in_board_scheme)
        ledDisplay.start_led_display_every(self.led_display_cycle_time)
