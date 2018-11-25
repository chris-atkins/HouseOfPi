#!env/bin/python
from app.server.hardware_interface import HardwareInterface 
from app.hardware.timed_LED_display import TimedLEDDisplay
from app.hardware.wink_display import WinkDisplay
from app.hardware.motion_sensor import MotionSensor

class HouseOfPi(HardwareInterface):

    def __init__(self, gpio_factory, motion_sensing_cycle_time = .1):
        super(HouseOfPi, self).__init__()
        
        self.led_display_cycle_time = 2
        self.motion_sensing_cycle_time = motion_sensing_cycle_time

        self.GPIO = gpio_factory.getGPIO()
        self.GPIO.setmode(self.GPIO.BOARD)

        self.GREEN_LED = 11
        self.GPIO.setup(self.GREEN_LED, self.GPIO.OUT)

        self.BLUE_LED = 13
        self.GPIO.setup(self.BLUE_LED, self.GPIO.OUT)

        self.IR_SENSOR = 16
        self.GPIO.setup(self.IR_SENSOR, self.GPIO.IN)
        

    def start_displaying_on_state(self, channel=11):
        led_display = TimedLEDDisplay(self.GPIO, channel)
        led_display.start_led_display_every(self.led_display_cycle_time)

    def blink_n_times_in_time(self, number_of_blinks, seconds_to_blink, channel=13):
        wink_display = WinkDisplay(self.GPIO, channel)
        wink_display.wink(number_of_blinks, seconds_to_blink)

    def start_motion_sensing(self, ir_sensor_channel=16, output_led_channel=13):
        motion_sensor = MotionSensor(gpio=self.GPIO, ir_sensor_channel=ir_sensor_channel, output_led_channel=output_led_channel)
        motion_sensor.start_motion_sensing(sensing_cycle_time=self.motion_sensing_cycle_time)
        