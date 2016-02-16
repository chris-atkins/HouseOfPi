#!env/bin/python

from gpiocrust import Header, OutputPin  # @UnresolvedImport
import time
import threading

with Header() as header:
    light = OutputPin(11)
    light.value = False
    
    def display_on_every(seconds):
        waitTime = seconds - .25
        while True:
            light.value = True
            time.sleep(.25)
            light.value = False
            time.sleep(waitTime)
            
    def start_server_on_display_every(seconds):
        t = threading.Thread(target=display_on_every, kwargs={'seconds': seconds})
        t.daemon = True
        t.start()    
        

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