class GPIOFactory(object):
    '''
        strategy and comments lifted from the authors of gpiocrust (thanks, nice work! :) - https://github.com/zourtney/gpiocrust
    '''

    def __init__(self):
        try:
            import RPi.GPIO as GPIO
            self.gpio = GPIO            
        except RuntimeError:
            print(
            '----------------------------------------------------------------------------')
            print(
            ' WARNING: RPi.GPIO can only be run on the RPi. Falling back to mock objects.')
            print(
            '----------------------------------------------------------------------------')
            self.gpio = EmptyGPIO()
        except ImportError:
            print('-------------------------------------------------------------------')
            print(' WARNING: RPi.GPIO library not found. Falling back to mock objects.')
            print('-------------------------------------------------------------------')
            self.gpio = EmptyGPIO()
            
    def getGPIO(self):
        return self.gpio


class EmptyGPIO(object):
    
#     global OUT, IN, HIGH, LOW 
    def __init__(self):
        self.OUT = 'OUT'
        self.IN = 'IN'
        self.HIGH = 'HIGH'
        self.LOW = 'LOW'
        self.BCM = 'BCM'
        self.BOARD = 'BOARD'
            
    def setup(self, channel, in_or_out):
        pass
    
    def cleanup(self, channels=[]):
        pass
    
    def output(self, channel, high_or_low):
        pass
    
    def setmode(self, mode):
        pass

    def input(self, channel):
        pass
    