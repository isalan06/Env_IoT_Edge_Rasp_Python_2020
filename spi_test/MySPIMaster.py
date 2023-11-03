#!/usr/bin/python3
#MySPIMaster.py

import spidev
import time
spi=spidev.SpiDev()
spi.open(1000000, 0)
print(spi.mode)
message = []
message.append(65)
message.append(48)
message.append(77)
message.append(49)
message.append(10)
print("Start Communication")
while 1:
    spi.writebytes(message)
    time.sleep(5)
    print("Next")
