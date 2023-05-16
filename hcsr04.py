import time
from machine import Pin, time_pulse_us

class HCSR04:
    def __init__(self, trig_pin, echo_pin, echo_timeout=25000):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.trig.value(0)
        
        self.echo = Pin(echo_pin, Pin.IN, Pin.PULL_DOWN)
        
    def distance_cm(self):
        self.trig.value(0)
        time.sleep(0.1)
        self.trig.value(1)
        time.sleep_us(2)
        self.trig.value(0)
        pulse_duration = time_pulse_us(self.echo, 1, 25000)
        distance = pulse_duration * 17165 / 1000000
        distance = round(distance, 0)
        return int(distance)
