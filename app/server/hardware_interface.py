#!env/bin/python
from abc import ABCMeta, abstractmethod

class HardwareInterface(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def start_displaying_on_state(self):
        pass