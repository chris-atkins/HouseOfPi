#!env/bin/python
from test_server_setup import buildTestServer
from flask_testing import LiveServerTestCase  # @UnresolvedImport
from mock_services.test_gpio import GPIOTestFactory
import time

class BlinkOnMotionTest(LiveServerTestCase):

    def create_app(self):
        self.LED = 13;
        self.IR_SENSOR = 16

        self.gpio_factory = GPIOTestFactory( track_gpio_calls = False)
        self.gpio = self.gpio_factory.getGPIO()
        return buildTestServer(gpioFactory=self.gpio_factory)

    def test_setup_called_on_correct_led_pin(self):
        self.assertTrue(self.gpio.setup_was_called_as_output_for_channel(self.LED))

    def test_setup_called_on_correct_ir_sensor_pin(self):
        self.assertTrue(self.gpio.setup_was_called_as_input_for_channel(self.IR_SENSOR))

    def test_led_turns_on_when_ir_sensor_input_is_high(self):
        self.gpio.simulate_high_input_on_pin(self.IR_SENSOR)
        print('pre-sleep')
        time.sleep(0.2)
        print('done-sleeping')
        # self.assertTrue(self.gpio.number_of_high_calls_for_channel(self.LED) == 1)
        # self.assertTrue(self.gpio.number_of_low_calls_for_channel(self.LED) == 0)

        self.gpio.simulate_low_input_on_pin(self.IR_SENSOR)
        time.sleep(0.2)
        # self.assertTrue(self.gpio.number_of_high_calls_for_channel(self.LED) == 1)
        # self.assertTrue(self.gpio.number_of_low_calls_for_channel(self.LED) == 1)
