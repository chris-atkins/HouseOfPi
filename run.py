#!env/bin/python
from app.server import app
import os
from app.hardware import app_status_display

debugOn = os.environ.get('PYTHON_DEBUG_ON')

app.config.update(dict(
    MY_HOUSE_URL='https://poorknight.com'
))

app_status_display.start_server_on_display_every(2)

if debugOn != None and (debugOn.lower() == 'true' or debugOn.lower() == 'yes'):
    app.run(debug=True, host='0.0.0.0')
else:
    app.run(debug=False, host='0.0.0.0')
