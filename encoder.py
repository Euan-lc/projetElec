from machine import Pin


class Encoder:
    def __init__(self, a, b, c, d):
        self.A = Pin(a, Pin.OUT)
        self.B = Pin(b, Pin.OUT)
        self.C = Pin(c, Pin.OUT)
        self.D = Pin(d, Pin.OUT)
#         self.segOne = Pin(segOne, Pin.OUT)
        #self.segOne = Pin(seg1, Pin.OUT)
        #self.segTwo = Pin(seg2, Pin.OUT)

    def writetoenc(self, num):
        formed = f"{num:04b}"
        
        print(formed)
        
        self.A.value(int(formed[3]))
        self.B.value(int(formed[2]))
        self.C.value(int(formed[1]))
        self.D.value(int(formed[0]))

#     def select(self, seg):
#         if seg == 1:
            # write to seg 0
#             self.segTwo.value(0)
#             self.segOne.value(1)

#         elif seg == 2:
            # write to seg 1
#             self.segOne.value(0)
#             self.segTwo.value(1)
# 
#         else:
#             print("no such segment")
