#!env/bin/python
import time
import threading

class MotionSensor(object):

    def __init__(self, gpio, ir_sensor_channel, output_led_channel):
        self.gpio = gpio
        self.ir_sensor_channel = ir_sensor_channel
        self.output_led_channel = output_led_channel

    def start_motion_sensing(self, sensing_cycle_time):
        t = threading.Thread(target=self.monitor_motion_every, kwargs={'sensing_cycle_time': sensing_cycle_time})
        t.daemon = True
        t.start()

    def monitor_motion_every(self, sensing_cycle_time):
        try:
            while True:
                time.sleep(sensing_cycle_time)

                motion_sensed = self.gpio.input(self.ir_sensor_channel)
                led_is_on = self.gpio.input(self.output_led_channel)
                if motion_sensed and not led_is_on:
                    self.gpio.output(self.output_led_channel, self.gpio.HIGH)
                elif not motion_sensed and led_is_on:
                    self.gpio.output(self.output_led_channel, self.gpio.LOW)
        finally:
            self.GPIO.cleanup(self.ir_sensor_channel)
            self.GPIO.cleanup(self.output_led_channel)
