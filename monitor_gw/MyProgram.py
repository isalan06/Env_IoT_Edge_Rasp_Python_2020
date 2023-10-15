#!/usr/bin/python3
#MyProgram.py

import MyPrint
import MyMiTempReader 
import MyDHT22Reader 
import MyThermalReader
import MyVibrationReader
import MyCameraReader
import MyParameterOperator
import time

SystemInfoString = 'System Info'

bRunning = True

if __name__ == "__main__":
    MyPrint.Print_Red('Start program to capture sensors.....')

    MyParameterOperator.ParameterOPInstance.LoadParameter()
    MyParameterOperator.ParameterOPInstance.LoadParameter2()

    myBLEDevice = MyMiTempReader.BLEDeviceForMi(True)
    myBLEDevice.Start()

    myDHT22Reader = MyDHT22Reader.DHT22Reader()
    myDHT22Reader.Start()
    myDHT22Reader.Read()

    myThermalReader = MyThermalReader.ThermalReader()
    myThermalReader.Start()
    myThermalReader.Read()

    myVibrationReader = MyVibrationReader.VibrationReader()
    myVibrationReader.Start()
    myVibrationReader.Read()

    myCameraReader = MyCameraReader.CameraReader()
    myCameraReader.Start()

    try:
        while bRunning:




            time.sleep(1.0)


        MyPrint.Print_Yellow("Main Threading is finished!", SystemInfoString)
    except KeyboardInterrupt:
        bRunning=False

    bRunning=False

    myCameraReader.Stop()
    myBLEDevice.Stop()

    MyPrint.Print_Green('Main Program is finished!', SystemInfoString)