#!env/bin/python
import os
from app.server.server import Server
from app.server.api import initRoutes
from app.hardware.house_of_pi import HouseOfPi
from app.hardware.gpio_factory import GPIOFactory

debugOn = os.environ.get('PYTHON_DEBUG_ON')

gpioFactory = GPIOFactory()
hardware = HouseOfPi(gpioFactory)
app = Server(__name__, hardware)

app.config.update(dict(
    MY_HOUSE_URL='https://poorknight.com',
    THERMOSTAT_URL='http://thermostat-76-B6-35',
    LIGHTS_URL='http://Philips-hue'
))

initRoutes(app)

if debugOn != None and (debugOn.lower() == 'true' or debugOn.lower() == 'yes'):
    app.run(debug=True, host='0.0.0.0')
else:
    app.run(debug=False, host='0.0.0.0')
