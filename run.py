#!env/bin/python
import os
from app.server.server import Server
from app.server.api import initRoutes
from app.hardware import app_status_display
from app.hardware.house_of_pi import HouseOfPi

debugOn = os.environ.get('PYTHON_DEBUG_ON')

hardware = HouseOfPi()
app = Server(__name__, hardware)

app.config.update(dict(
    MY_HOUSE_URL='https://poorknight.com'
))

initRoutes(app)

app_status_display.start_server_on_display_every(2)

if debugOn != None and (debugOn.lower() == 'true' or debugOn.lower() == 'yes'):
    app.run(debug=True, host='0.0.0.0')
else:
    app.run(debug=False, host='0.0.0.0')
