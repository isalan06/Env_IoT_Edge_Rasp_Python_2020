#!/usr/bin/python3
#MyProgram.py

import MyPrint
import MyMiTempReader 
import MyDHT22Reader 
import time

if __name__ == "__main__":
    MyPrint.Print_Red('test')

    myBLEDevice = MyMiTempReader.BLEDeviceForMi(True)
    myBLEDevice.Start()

    myDHT22Reader = MyDHT22Reader.DHT22Reader()
    myDHT22Reader.Start()
    myDHT22Reader.Read()

    time.sleep(30.0)

    myBLEDevice.Stop()

    MyPrint.Print_Green('finish')