import RPi.GPIO as g
import time
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [24, 25, 8, 7, 12, 16, 20, 21]

def dec2bin(a):
    return [int(i) for i in bin(a)[2:].zfill(8)]
def bin2dac(a):
    signal = dec2bin(a)
    g.output(dac, signal)
    return signal

troykaModule = 17

g.setmode(g.BCM)
g.setup(dac, g.OUT, initial = g.LOW)
g.setup(leds, g.OUT, initial = g.LOW)
g.setup(troykaModule, g.OUT, initial  = g.HIGH)
g.setup(4, g.IN)


try:
    while True:
        ar = [0, 0, 0, 0, 0, 0, 0, 0]
        b = 0
        c = 0
        for i in range(8):
            c += 2**(7 - i)
            signal = bin2dac(c)
            time.sleep(0.001)
            compvalue = g.input(4)
            if compvalue == 0:
                ar[i] = 0
                c -= 2**(7 - i)
            else:
                ar[i] = 1
                b += 2**(7 - i)
        V = (b / 256) * 3.3
        print("Digital Value : {}, input voltage = {:.2f}".format(b, V))
        j = b / 32
        ar = [1, 1, 1, 1, 1, 1, 1, 1]
        for i in range(7, int(j), -1):
            ar[i] = 0
        if b == 0:
            g.output(leds, g.LOW)
        else:
            g.output(leds, ar)
        #print(ar)
finally:
    g.output(dac, g.LOW)
    g.cleanup()