from machine import Pin, Timer
import time
from hcsr04 import HCSR04
import sys
import select
from encoder import Encoder
from picozero import Pot

greenLed = Pin(12, Pin.OUT)
redLed = Pin(13, Pin.OUT)
setButton = Pin(7, Pin.IN)
potentiometer = Pot(0)
segOff = Pin(15, Pin.OUT)

greenLed.value(1)
redLed.value(0)


enc = Encoder(21, 18, 19, 20)

poll_object = select.poll()
poll_object.register(sys.stdin, 1)

hc = HCSR04(16, 17)

distance = 0
maximum = 20

flickerBool = False
measureTimerSwitch = True
measureTimer = Timer()

def measureDistance(timer):
    global maximum
    global measureTimerSwitch
    global flickerBool
    if measureTimerSwitch:
        segOff.value(True)
        distance = hc.distance_cm()
        if (int(distance) > int(maximum)):
            greenLed.value(0)
            redLed.value(1)
        else:
            greenLed.value(1)
            redLed.value(0)
        print(distance)
        enc.writetoenc(int(str(distance)[-1]))
    else:
        potValue = int(translate(potentiometer.value, 0.06, 1, 2, 200))
        print(potValue)
        maximum=potValue
        enc.writetoenc(int(str(potValue)[-1]))
        segOff.value(flickerBool)
        flickerBool = not flickerBool

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

measureTimer.init(period=200, callback=measureDistance)

while True:
    if poll_object.poll(0):
        line = sys.stdin.buffer.readline()
        stripped = line.strip()
        maximum = int(stripped)
    if setButton.value():
        time.sleep(0.5)
        measureTimerSwitch = not measureTimerSwitch
        time.sleep(0.5)

