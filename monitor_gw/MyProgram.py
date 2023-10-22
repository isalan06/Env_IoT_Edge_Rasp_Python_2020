#!/usr/bin/python3
#MyProgram.py

import MyPrint
import MyMiTempReader 
import MyDHT22Reader 
from MyDHT22Reader import DHT22Data
import MyThermalReader
from MyThermalReader import ThermalData
import MyVibrationReader
from MyVibrationReader import VibrationData
import MyCameraReader
import MyParameterOperator
import time
import threading

SystemInfoString = 'System Info'

bRunning = True
bCaptureData = False

def DoCapture():
    global bCaptureData
    global bRunning
    
    while bRunning:
        if DHT22Data.bDHT22DeviceExist:
            myDHT22Reader.Read()

        if VibrationData.bAccelGaugeDeviceExist:
            myVibrationReader.Read()

        if ThermalData.bThermalCameraExist:
            myThermalReader.Read()

        bCaptureData = True

        time.sleep(MyParameterOperator.ParameterData.GeneralParameter.SensorsFValue)



    pass

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

    myCaptureThread = threading.Thread(target=DoCapture)
    myCaptureThread.Start()

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