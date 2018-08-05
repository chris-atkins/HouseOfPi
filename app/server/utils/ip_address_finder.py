#!env/bin/python

import requests

class IpAddressFinder():

    def __init__(self, config):
        self.ip_address = config.get('IP_ADDRESS_URL')

    def find_current_ip_address(self):
        url = self.ip_address + '?format=json'
        response = requests.get(url=url)
        return response.json()['ip']



