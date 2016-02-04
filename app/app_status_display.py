#!env/bin/python

from gpiocrust import Header, OutputPin
import time
import threading

with Header() as header:
    light = OutputPin(11)
    light.value = False
    
    def display_on_every(seconds):
        while True:
            light.value = True
            time.sleep(.5)
            light.value = False
            time.sleep(seconds - .5)
            
    def start_server_on_display_every(seconds):
        t = threading.Thread(target=display_on_every, kwargs={'seconds':'5'})
        t.daemon = True
        t.start()    
        