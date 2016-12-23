#!env/bin/python
from test_server_setup import buildTestServer
from test_server_setup import myHouseUrl
from test_server_setup import authenticationSecret
from flask.ext.testing import LiveServerTestCase  # @UnresolvedImport
import requests  # @UnresolvedImport

class TextMeIntegrationTestCase(LiveServerTestCase):

    def create_app(self):
        return buildTestServer()

    def test_mock_service_is_up(self):
        response = requests.get(myHouseUrl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Server is up')

    def test_text_me_calls_mock_with_correct_json(self):
        requests.get(self.get_server_url() + '/textMe', headers={'auth-secret': authenticationSecret})
        sentToMyHouseResponse = requests.get(myHouseUrl + '/lastNotificationMessage')
        
        expectedSentRequest = {"messageContent":"Raspberry Pi says hi and would like to inform you that it was asked to send you a message."}
        self.assertEquals(sentToMyHouseResponse.json(), expectedSentRequest)

    def test_text_me_returns_message_from_remote_server(self):
        response = requests.get(self.get_server_url() + '/textMe', headers={'auth-secret': authenticationSecret})
        self.assertEquals(response.text, 'Notify stub response')

    def test_wink_endpoint_requires_authentication_header_with_secret(self):
        response = requests.get(self.get_server_url() + '/textMe')
        self.assertEqual(response.status_code, 401)

