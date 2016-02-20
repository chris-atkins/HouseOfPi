import pickle

class GPIOTestFactory(object):

    def __init__(self, track_gpio_calls):
        self.gpio = TestGPIO(track_gpio_calls=track_gpio_calls)            
            
    def getGPIO(self):
        return self.gpio


class TestGPIO(object):
    
    def __init__(self, track_gpio_calls):
        self.should_save_status = track_gpio_calls
        self.channel_output_high_calls = {}
        self.channel_output_low_calls = {}
        self.setup_called_on_channel_list = []
        self.set_pin_mode_called_value = 'NOT CALLED'
        self.OUT = 'OUT'
        self.IN = 'IN'
        self.HIGH = 'HIGH'
        self.LOW = 'LOW'
        self.BCM = 'BCM'
        self.BOARD = 'BOARD'
    
    def setmode(self, mode):
        self.set_pin_mode_called_value = mode;
    
    def setup(self, channel, in_or_out):
        print('setup called for channel: ' + str(channel) + " as " + str(in_or_out))
        
        if channel in self.channel_output_high_calls.keys():
            raise Exception('The channel is already setup: ' + str(channel))
        
        self.channel_output_high_calls[channel] = 0
        self.channel_output_low_calls[channel] = 0
        self.setup_called_on_channel_list.append(channel)
        self.save_status()
        
    
    def cleanup(self, channels=[]):
        print('cleanup called for channel: ' + str(channels))
    
    
    def output(self, channel, high_or_low):
        if high_or_low == self.HIGH:
            self.channel_output_high_calls[channel] += 1
            
        if high_or_low == self.LOW:
            self.channel_output_low_calls[channel] += 1
            
        self.save_status()
    
#######################################################################     
    
    def number_of_high_calls_for_channel(self, channel):
        return self.channel_output_high_calls[channel]
    
    def number_of_low_calls_for_channel(self, channel):
        return self.channel_output_low_calls[channel]
    
    def setup_was_called_for_channel(self, channel):
        return channel in self.setup_called_on_channel_list
    
    def gpio_pin_mode_setting(self):
        return self.set_pin_mode_called_value
    
    def save_status(self):
        if self.should_save_status:
            print('saving gpio status')
            with open('gpio.pickle', 'wb') as f:
                pickle.dump(self, f)
