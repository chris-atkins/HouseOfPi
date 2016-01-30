#!env/bin/python
from app import app
import os

debugOn = os.environ.get('PYTHON_DEBUG_ON')

if debugOn != None and (debugOn.lower() == 'true' or debugOn.lower() == 'yes'):
    app.run(debug=True, host='0.0.0.0')
else:
    app.run(host='0.0.0.0')