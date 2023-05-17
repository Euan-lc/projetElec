from machine import Pin
from time import sleep


class Encoder:
    def __init__(self, a, b, c, d, seg1, seg2):
        self.A = Pin(a, Pin.OUT)
        self.B = Pin(b, Pin.OUT)
        self.C = Pin(c, Pin.OUT)
        self.D = Pin(d, Pin.OUT)

        self.segOne = Pin(seg1, Pin.OUT)
        self.segTwo = Pin(seg2, Pin.OUT)

    def write_to_enc(self, num):
        formed = f"{int(num):04b}"

        self.A.value(int(formed[3]))
        self.B.value(int(formed[2]))
        self.C.value(int(formed[1]))
        self.D.value(int(formed[0]))

    def select(self, seg):
        if seg == 1:
            self.segTwo.value(0)
            self.segOne.value(1)

        elif seg == 2:
            self.segOne.value(0)
            self.segTwo.value(1)

    def convert_to_double_digit(self, num):
        num_digits = len(str(num))
        if num_digits == 1:
            return "0" + str(num)
        elif num_digits == 2:
            return str(num)
        elif num_digits == 3:
            return str(round(float(num) / 100, 1))

    def write_double(self, num):
        digit_str = self.convert_to_double_digit(num)
        self.select(1)
        self.write_to_enc(digit_str[-1])
        sleep(0.01)
        self.select(2)
        self.write_to_enc(digit_str[0])
        sleep(0.01)
