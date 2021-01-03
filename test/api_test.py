#!env/bin/python
import unittest
from test_server_setup import buildTestServer, authenticationSecret


class MockWemo(object):

    last_brightness = -1

    def set_brightness(self, brightness):
        MockWemo.last_brightness = brightness


class MyTestCase(unittest.TestCase):

    def setup_class(self):
        mock_wemo = MockWemo()
        self.app = buildTestServer(wemoDevices=[mock_wemo]).test_client()

    def test_client_directly(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.data, b'Hi there!')

    def test_command_with_lights_off_includes_setting_wemo(self):
        response = self.app.put('/house/command', json={"command": "lights-off"}, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(MockWemo.last_brightness, 0)

    def test_command_with_lights_on_includes_setting_wemo(self):
        response = self.app.put('/house/command', json={"command": "lights-on"}, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(MockWemo.last_brightness, 70)

    def test_command_with_lights_dim_includes_setting_wemo(self):
        response = self.app.put('/house/command', json={"command": "dim-lights"}, headers={'auth-secret': authenticationSecret})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(MockWemo.last_brightness, 25)
