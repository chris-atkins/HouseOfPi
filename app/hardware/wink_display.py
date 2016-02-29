#!env/bin/python
import time
import threading

class WinkDisplay(object):

    def __init__(self, GPIO, channel):
        self.GPIO = GPIO
        self.channel = channel

    def wink(self, number_of_blinks, seconds_to_blink):
        t = threading.Thread(target=self.display_on_every, kwargs={'number_of_blinks': number_of_blinks, 'seconds_to_blink': seconds_to_blink})
        t.daemon = True
        t.start()      

    def display_on_every(self, number_of_blinks, seconds_to_blink):
        led_blink_time = seconds_to_blink / number_of_blinks / 2.0
        for i in range(0, number_of_blinks):
            self.GPIO.output(self.channel, self.GPIO.HIGH)
            time.sleep(led_blink_time)
            self.GPIO.output(self.channel, self.GPIO.LOW)
            time.sleep(led_blink_time)
