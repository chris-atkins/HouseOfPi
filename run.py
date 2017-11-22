#!env/bin/python
import os
from app.server.server import Server
from app.server.api import initRoutes
from app.hardware.house_of_pi import HouseOfPi
from app.hardware.gpio_factory import GPIOFactory

debugOn = os.environ.get('PYTHON_DEBUG_ON')
sslOn = os.environ.get('PYTHON_SSL_ON')

gpioFactory = GPIOFactory()
hardware = HouseOfPi(gpioFactory)
app = Server(__name__, hardware)

app.config.update(dict(
    MY_HOUSE_URL='https://poorknight.com',
    THERMOSTAT_URL='http://10.0.0.114',
    LIGHTS_URL='http://10.0.0.196',
    AUTHENTICATION_SECRET=os.environ.get('AUTHENTICATION_SECRET')
))

initRoutes(app)

if debugOn is not None and (debugOn.lower() == 'true' or debugOn.lower() == 'yes'):
    print('STARTING SERVER IN DEBUG MODE')
    app.run(host='0.0.0.0', port=5000, debug=True)

elif sslOn is not None and (sslOn.lower() == 'true' or sslOn.lower() == 'yes'):
    print('STARTING SERVER WITH SSL ENABLED')
    context = ('cert.crt', 'key.key')
    app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=False)

else:
    print('STARTING SERVER WITH NO SSL')
    app.run(host='0.0.0.0', port=5000, debug=False)
