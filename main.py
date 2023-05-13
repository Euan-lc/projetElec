from machine import Pin, Timer
import time
from hcsr04 import HCSR04
import sys
import select
from encoder import Encoder

time.sleep(1)
greenLed = Pin(12, Pin.OUT)
redLed = Pin(13, Pin.OUT)

greenLed.value(1)
redLed.value(0)

enc = Encoder(21, 18, 19, 20)

poll_object = select.poll()
poll_object.register(sys.stdin, 1)

hc = HCSR04(16, 17)

distance = 0
maximum = 20

tim = Timer()

def tick(timer):
    global maximum
    
    distance = hc.distance_cm()
    if (int(distance) > int(maximum)):
        greenLed.value(0)
        redLed.value(1)
    else:
        greenLed.value(1)
        redLed.value(0)

    print(distance)
    enc.writetoenc(int(str(distance)[-1]))

tim.init(period=200, callback=tick)

while True:
    if poll_object.poll(0):
        line = sys.stdin.buffer.readline()
        stripped = line.strip()
        maximum = int(stripped)