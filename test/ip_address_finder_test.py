#!env/bin/python
import unittest

from app.server.utils.ip_address_finder import IpAddressFinder

class IpAddressFinderTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_GPIO_setup_in_board_config(self):
        config = {'IP_ADDRESS_URL': 'http://127.0.0.1:6234'} # mock ip address server
        ip_address_finder = IpAddressFinder(config)
        ip_address = ip_address_finder.find_current_ip_address()
        self.assertEquals(ip_address, '1.2.3.4') #mock server is set up to use this

