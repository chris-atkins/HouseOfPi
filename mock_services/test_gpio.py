import pickle

class GPIOTestFactory(object):

    def __init__(self, track_gpio_calls):
        self.gpio = TestGPIO(track_gpio_calls=track_gpio_calls)            
            
    def getGPIO(self):
        return self.gpio


class TestGPIO(object):
    
    def __init__(self, track_gpio_calls):
        print('constructing a new test GPIO')
        self.should_save_status = track_gpio_calls
        self.channel_output_high_calls = {}
        self.channel_output_low_calls = {}
        self.setup_as_output_called_on_channel_list = []
        self.setup_as_input_called_on_channel_list = []
        self.should_return_high_for_channel_list = []
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

        if in_or_out == self.IN:
            self.setup_as_input_called_on_channel_list.append(channel)
        elif in_or_out == self.OUT:
            self.setup_as_output_called_on_channel_list.append(channel)
        else:
            raise Exception('No valid in_or_out was sent when setting up a pin on the GPIO.  Value received was: ' + str(in_or_out))

        self.save_status()
        
    
    def cleanup(self, channels=[]):
        print('cleanup called for channel: ' + str(channels))


    def input(self, channel):
        # print('looking for ' + str(channel) + ' in ' + str(self.should_return_high_for_channel_list))
        should_return_high = channel in self.should_return_high_for_channel_list
        if should_return_high:
            # print('returning 1 for channel input request')
            return 1
        else:
            # print('returning 0 for channel input request')
            return 0


    def output(self, channel, high_or_low):
        if high_or_low == self.HIGH:
            self.channel_output_high_calls[channel] += 1
            self.simulate_high_input_on_pin(channel)
            # print("Saving HIGH for channel " + str(channel) + ' | ' + str(self.channel_output_high_calls[channel]))

        if high_or_low == self.LOW:
            self.channel_output_low_calls[channel] += 1
            self.simulate_low_input_on_pin(channel)
            # print("Saving LOW for channel " + str(channel) + '  | ' + str(self.channel_output_low_calls[channel]))

        self.save_status()


    def simulate_high_input_on_pin(self, channel):
        if channel not in self.should_return_high_for_channel_list:
            # print('adding channel to list: ' + str(channel))
            self.should_return_high_for_channel_list.append(channel)
        # print('current list after simulate high called: ' + str(self.should_return_high_for_channel_list))


    def simulate_low_input_on_pin(self, channel):
        if channel in self.should_return_high_for_channel_list:
            # print('removing channel from list: ' + str(channel))
            self.should_return_high_for_channel_list.remove(channel)
        # print('current list after simulate low called: ' + str(self.should_return_high_for_channel_list))

#######################################################################     
    
    def number_of_high_calls_for_channel(self, channel):
        # print('reporting HIGH calls: ' + str(self.channel_output_high_calls[channel]))
        return self.channel_output_high_calls[channel]
    
    def number_of_low_calls_for_channel(self, channel):
        # print('reporting LOW calls: ' + str(self.channel_output_low_calls[channel]))
        return self.channel_output_low_calls[channel]
    
    def setup_was_called_as_output_for_channel(self, channel):
        return channel in self.setup_as_output_called_on_channel_list

    def setup_was_called_as_input_for_channel(self, channel):
        return channel in self.setup_as_input_called_on_channel_list
    
    def gpio_pin_mode_setting(self):
        return self.set_pin_mode_called_value
    
    def save_status(self):
        if self.should_save_status:
            # print('saving gpio status')
            with open('gpio.pickle', 'wb') as f:
                pickle.dump(self, f)
