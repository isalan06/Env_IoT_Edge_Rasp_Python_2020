#!/usr/bin/python3
#MyProgram.py

import MyPrint
from MiTempReader import BLEDeviceForMi
import time

if __name__ == "__main__":
    MyPrint.Print_Red('test')

    myBLEDevice = BLEDeviceForMi(True)
    myBLEDevice.Start()

    time.sleep(30.0)

    myBLEDevice.Stop()

    MyPrint.Print_Green('finish')