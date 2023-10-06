#!/usr/bin/python3
#MyProgram.py

import MyPrint
import MyMiTempReader 
import MyDHT22Reader 
import MyThermalReader
import MyVibrationReader
import time

bRunning = True

if __name__ == "__main__":
    MyPrint.Print_Red('test')

    myBLEDevice = MyMiTempReader.BLEDeviceForMi(True)
    myBLEDevice.Start()

    myDHT22Reader = MyDHT22Reader.DHT22Reader()
    myDHT22Reader.Start()
    myDHT22Reader.Read()

    myThermalReader = MyThermalReader.ThermalReader()
    myThermalReader.Start()
    myThermalReader.Read()

    myVibrationReader = MyVibrationReader()
    myVibrationReader.Start()
    myVibrationReader.Read()

    try:
        while bRunning:




            time.sleep(1.0)


        MyPrint.Print_Yellow("[System]Main Threading is finished!")
    except KeyboardInterrupt:
        bRunning=False

    bRunning=False

    myBLEDevice.Stop()

    MyPrint.Print_Green('finish')