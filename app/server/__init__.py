#!env/bin/python
from app.server.server import Server
from app.hardware.house_of_pi import HouseOfPi

app = Server(__name__, HouseOfPi())

from app.server import api  