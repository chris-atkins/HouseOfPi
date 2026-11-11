#!env/bin/python
import os
from app.server.server import Server
from app.server.api import initRoutes
from app.server.scheduled_jobs import init_scheduled_jobs
from app.server.server_options import server_options_from_env
from app.hardware.house_of_pi import HouseOfPi
from app.hardware.gpio_factory import GPIOFactory
import pywemo

options = server_options_from_env(os.environ)

wemoDevices = pywemo.discover_devices()
gpioFactory = GPIOFactory()
hardware = HouseOfPi(gpioFactory)
app = Server(__name__, hardware, wemoDevices)

app.config.update(dict(
    MY_HOUSE_URL='https://poorknight.com',
    THERMOSTAT_URL='http://192.168.1.3',
    LIGHTS_URL='http://192.168.1.9',
    IP_ADDRESS_URL='https://api.ipify.org',
    SECONDS_BETWEEN_IP_REPORTS='300',
    AUTHENTICATION_SECRET=os.environ.get('AUTHENTICATION_SECRET')
))

initRoutes(app)
init_scheduled_jobs(app.config)

# flush: stdout is redirected to log.txt by the deploy, and the runbook checks for this line.
print(f'STARTING SERVER on {options.host}:{options.port} '
      f'(ssl={options.ssl_context is not None}, debug={options.debug})', flush=True)
app.run(host=options.host, port=options.port, ssl_context=options.ssl_context, debug=options.debug)
