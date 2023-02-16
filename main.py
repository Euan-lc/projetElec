from encoder import Encoder
from hcsr04 import HCSR04

a = 12
b = 13
c = 14
d = 15

seg1 = 16
seg2 = 17

seg1_value = 0
seg2_value = 0

trig = 18
echo = 1

enc = Encoder(a, b, c, d, seg1, seg2)
sens = HCSR04(trig, echo)

while True:
    distance = sens.distance_cm()
    if distance > 99:
        seg1_value = f'{distance:02d}'[0]
        seg2_value = f'{distance:02d}'[1]

    elif 99 < distance < 1000:
        seg1_value = f'{distance:.1f}'[0]
        seg2_value = f'{distance:.1f}'[1]
    else:
        print('uh oh poopy')

    enc.select(1)
    enc.writetoenc(seg1_value)
    enc.select(2)
    enc.writetoenc(seg2_value)
