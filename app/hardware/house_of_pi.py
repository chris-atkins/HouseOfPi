#!env/bin/python
from app.server.hardware_interface import HardwareInterface 
from app.hardware.timed_LED_display import TimedLEDDisplay
from app.hardware.wink_display import WinkDisplay

class HouseOfPi(HardwareInterface):

    def __init__(self, gpio_factory):
        super(HouseOfPi, self).__init__()
        
        self.led_display_cycle_time = 2
        
        self.GPIO = gpio_factory.getGPIO()
        self.GPIO.setmode(self.GPIO.BOARD)
        
        self.GREEN_LED = 11
        self.GPIO.setup(self.GREEN_LED, self.GPIO.OUT)
        
        self.BLUE_LED = 13
        self.GPIO.setup(self.BLUE_LED, self.GPIO.OUT)
        

    def start_displaying_on_state(self, channel=11):
        ledDisplay = TimedLEDDisplay(self.GPIO, channel)
        ledDisplay.start_led_display_every(self.led_display_cycle_time)

    def blink_n_times_in_time(self, number_of_blinks, seconds_to_blink, channel=13):
        winkDisplay = WinkDisplay(self.GPIO, channel)
        winkDisplay.wink(number_of_blinks, seconds_to_blink)
        