#!env/bin/python
from app import app
import os

debugOn = os.environ.get('PYTHON_DEBUG_ON')

app.config.update(dict(
    MY_HOUSE_URL='https://poorknight.com'
))
if debugOn != None and (debugOn.lower() == 'true' or debugOn.lower() == 'yes'):
    app.run(debug=True, host='0.0.0.0')
else:
    app.run(debug=False, host='0.0.0.0')