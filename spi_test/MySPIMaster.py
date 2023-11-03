#!/usr/bin/python3
#MySPIMaster.py

import spidev
import time
spi=spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000
print(spi.mode)
message = []
message.append(65)
message.append(48)
message.append(77)
message.append(49)
message.append(10)
print("Start Communication")
while 1:
    spi.xfer(message)
    time.sleep(5)
    print("Next")
