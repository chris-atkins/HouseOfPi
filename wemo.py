#!env/bin/python

import pywemo
import time

devices = pywemo.discover_devices()
print(devices)

dimmer = devices[0]

print("turning off lights")
dimmer.set_brightness(0)

time.sleep(3)
print("turning on lights")
dimmer.set_brightness(100)

time.sleep(3)

print("medium")
dimmer.set_brightness(50)

attrs = vars(dimmer)
print('\n'.join("%s: %s" % item for item in attrs.items()))

print(dimmer.name)