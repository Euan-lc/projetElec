from machine import Pin


class Encoder:
    def __init__(self, a, b, c, d, seg1, seg2):
        self.A = Pin(a, Pin.OUT)
        self.B = Pin(b, Pin.OUT)
        self.C = Pin(c, Pin.OUT)
        self.D = Pin(d, Pin.OUT)

        self.segOne = Pin(seg1, Pin.OUT)
        self.segTwo = Pin(seg2, Pin.OUT)

    def writetoenc(self, num):
        formed = f"{num:04b}"

        self.A.value(formed[0])
        self.B.value(formed[1])
        self.C.value(formed[2])
        self.D.value(formed[3])

    def select(self, seg):
        if seg == 1:
            # write to seg 0
            self.segTwo.value(0)
            self.segOne.value(1)

        elif seg == 2:
            # write to seg 1
            self.segOne.value(0)
            self.segTwo.value(1)

        else:
            print("no such segment")
