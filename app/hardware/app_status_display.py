#!env/bin/python
import time
import threading

class TimedLEDDisplay(object):
    
    def __init__(self, GPIO, channel_in_board_scheme):
        self.GPIO = GPIO
        self.channel = channel_in_board_scheme
        self.GPIO.setup(self.channel, self.GPIO.OUT)
    
    def start_led_display_every(self, seconds_per_cycle, seconds_led_is_on = .25):
        t = threading.Thread(target=self.display_on_every, kwargs={'seconds_per_cycle': seconds_per_cycle, 'seconds_led_is_on': seconds_led_is_on})
        t.daemon = True
        t.start()      
        
    def display_on_every(self, seconds_per_cycle, seconds_led_is_on):
        waitTime = seconds_per_cycle - seconds_led_is_on
        try:
            while True:
                self.GPIO.output(self.channel, self.GPIO.HIGH)
                time.sleep(seconds_led_is_on)
                self.GPIO.output(self.channel, self.GPIO.LOW)
                time.sleep(waitTime)
        finally:
            self.GPIO.cleanup(self.channel)