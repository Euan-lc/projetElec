from machine import Pin, Timer
import time
from hcsr04 import HCSR04
import sys
import select
from encoder import Encoder
from picozero import Pot

greenLed = Pin(12, Pin.OUT)
redLed = Pin(13, Pin.OUT)
setButton = Pin(11, Pin.IN)
potentiometer = Pot(0)
segOff = Pin(15, Pin.OUT)
greenLed.value(1)
redLed.value(0)

enc = Encoder(21, 18, 19, 20, 9, 22)

poll_object = select.poll()
poll_object.register(sys.stdin, 1)

hc = HCSR04(16, 17)

distance = 0
maximum = 20
toDisplay = 14
flickerBool = False
measureSwitch = True
measureTimer = Timer()


def measureDistance(timer):
    global maximum
    global flickerBool
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


measureTimer.init(period=25, callback=measureDistance)

while True:
    time.sleep(0.2)
    if poll_object.poll(0):
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
        toDisplay = hc.distance_cm()
    else:
        toDisplay = int(translate(potentiometer.value, 0.025, 0.97, 2, 200))
    print(("H" if measureSwitch else "M") + str(toDisplay))

