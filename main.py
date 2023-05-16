from machine import Pin, Timer
import time
import sys
import select

from hcsr04 import HCSR04
from encoder import Encoder
from picozero import Pot

greenLed = Pin(12, Pin.OUT)
redLed = Pin(13, Pin.OUT)

greenLed.value(0)
redLed.value(0)

setButton = Pin(11, Pin.IN)
potentiometer = Pot(0)

enc = Encoder(21, 18, 19, 20, 9, 22)

pollObject = select.poll()
pollObject.register(sys.stdin, 1)

HCSensor = HCSR04(16, 17)

maximum = 20
toDisplay = 14
measureSwitch = True
measureTimer = Timer()


def measure_distance(timer):
    global maximum
    global toDisplay
    global measureSwitch

    if measureSwitch:
        if (int(toDisplay) > int(maximum)):
            greenLed.value(0)
            redLed.value(1)
        else:
            greenLed.value(1)
            redLed.value(0)
    else:
        greenLed.value(1)
        redLed.value(1)
    enc.write_double(toDisplay)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


measureTimer.init(period=25, callback=measure_distance)

while True:
    time.sleep(0.2)
    if pollObject.poll(0):
        line = sys.stdin.buffer.readline()
        stripped = line.strip()
        maximum = int(stripped)
    if setButton.value():
        time.sleep(0.5)
        if not measureSwitch:
            maximum = int(translate(potentiometer.value, 0.025, 0.97, 2, 200))
        measureSwitch = not measureSwitch
        time.sleep(0.5)
    if measureSwitch:
        toDisplay = HCSensor.distance_cm()
    else:
        toDisplay = int(translate(potentiometer.value, 0.025, 0.97, 2, 200))
    print(("H" if measureSwitch else "M") + str(toDisplay))
