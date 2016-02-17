#!env/bin/python
import pickle

def load_tracked_gpio():
    with open('gpio.pickle', 'rb') as f:
        return pickle.load(f)  