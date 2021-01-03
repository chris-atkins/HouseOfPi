#!env/bin/python

import pywemo

devices = pywemo.discover_devices()
print(devices)

dimmer = devices[0]

dimmer.set_brightness(70)

attrs = vars(dimmer)
print('\n'.join("%s: %s" % item for item in attrs.items()))

print(dimmer.name)