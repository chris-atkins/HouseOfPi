#!env/bin/python
from app import app  # @UnresolvedImport
import os
from app import app_status_display


debugOn = os.environ.get('PYTHON_DEBUG_ON')

app.config.update(dict(
    MY_HOUSE_URL='https://poorknight.com'
))
if debugOn != None and (debugOn.lower() == 'true' or debugOn.lower() == 'yes'):
    app.run(debug=True, host='0.0.0.0')
else:
    app.run(debug=False, host='0.0.0.0')

app_status_display.display_on_for(1)
    
app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))