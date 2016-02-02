#!env/bin/python

from gpiocrust import Header, OutputPin
import time

with Header() as header:
    light = OutputPin(17)
    light.value = False
    
    def display_on_for(seconds):
        light.value = True
        time.sleep(seconds)
        light.value = False
        
        