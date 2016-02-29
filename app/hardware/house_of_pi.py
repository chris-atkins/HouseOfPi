#!env/bin/python
from app.server.hardware_interface import HardwareInterface 
from app.hardware.timed_LED_display import TimedLEDDisplay
import time

class HouseOfPi(HardwareInterface):

    def __init__(self, gpio_factory):
        super(HouseOfPi, self).__init__()
        self.led_display_cycle_time = 2
        self.GPIO = gpio_factory.getGPIO()
        self.GPIO.setmode(self.GPIO.BOARD)
        self.GREEN_LED = 11
        self.GPIO.setup(self.GREEN_LED, self.GPIO.OUT)
        

    def start_displaying_on_state(self, channel_in_board_scheme=11):
        ledDisplay = TimedLEDDisplay(self.GPIO, channel_in_board_scheme)
        ledDisplay.start_led_display_every(self.led_display_cycle_time)

    def blink_n_times_in_time(self, blink_times, seconds):
        led_blink_time = seconds / blink_times
        for i in range(0, blink_times):
            self.GPIO.output(11, self.GPIO.HIGH)
            time.sleep(led_blink_time)
            self.GPIO.output(11, self.GPIO.LOW)
            time.sleep(led_blink_time)
