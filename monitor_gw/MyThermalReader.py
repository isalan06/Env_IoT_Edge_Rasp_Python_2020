#!/usr/bin/python3
#MyThermalReader.py
#AMG8833

from Adafruit_AMG88xx import Adafruit_AMG88xx

import MyPrint

class ThermalDataDto:
    thermalpixels= []
    thermalmaxValue = 0.0
    thermalminValue = 0.0

    sThermalStatus = 'Stop'
    bThermalCameraExist = False

    def __init__(self):
        pass

ThermalData = ThermalDataDto()

class ThermalReader:

    thermalImage = 0

    def __init__(self):
        global ThermalData

        ThermalData.sThermalStatus = "Stop"
        ThermalData.bThermalCameraExist = False

    def Start(self):
        global thermalImage
        global ThermalData

        try:
            thermalImage = Adafruit_AMG88xx()
            MyPrint.Print_Green("[Thermal Info]Connect to Theraml Camera Success")
            ThermalData.sThermalStatus = "Running"
            ThermalData.bThermalCameraExist = True
        except:
            thermalImage = 0
            MyPrint.Print_Red("[Thermal Info]Connect to Theraml Camera Fail")
            ThermalData.sThermalStatus = "Stop"
            ThermalData.bThermalCameraExist = False
    
    def Read(self):
        global thermalImage
        global ThermalData

        try:
            if (thermalImage != 0) and ThermalData.bThermalCameraExist:
                ThermalData.thermalpixels = thermalImage.readPixels()
        except:
            MyPrint.Print_Red("[Thermal Info]Get TermalPixels Failure")