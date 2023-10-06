#!/usr/bin/python3
#MyDHT22Reader.py

import adafruit_dht
import board
import MyPrint

__DHT22InfoString = 'DHT22 Info'
__DHT22ErrorString = 'DHT22 Info'


class DHT22DataDto:
    temp_c = 0.0
    humidity = 0.0

    sDHT22Status = 'Stop'
    bDHT22DeviceExist = False

    def __init__(self):
        pass

DHT22Data = DHT22DataDto()

class DHT22Reader:

    dhtDevice = 0
  
    def __init__(self):

        global DHT22Data
        global dhtDevice

        dhtDevice = 0
        DHT22Data.sDHT22Status="Stop"
        DHT22Data.bDHT22DeviceExist = False

    def Start(self):
        global DHT22Data
        global dhtDevice

        try:
            dhtDevice = adafruit_dht.DHT22(board.D17)
            MyPrint.Print_Green("Create DHT Device Success", __DHT22InfoString)
            DHT22Data.sDHT22Status="Running"
            DHT22Data.bDHT22DeviceExist = True
        except:
            dhtDevice = 0
            MyPrint.Print_Red("Create DHT Device Fail", __DHT22ErrorString)
            DHT22Data.sDHT22Status="Stop"
            DHT22Data.bDHT22DeviceExist = False

    def Read(self):
        global DHT22Data
        global dhtDevice

        try:
            if dhtDevice != 0:
                DHT22Data.temp_c = dhtDevice.temperature
                DHT22Data.humidity = dhtDevice.humidity
            else:
                MyPrint.Print_Red("Get DHT Module did not exist", __DHT22ErrorString)
        except RuntimeError as error:
            MyPrint.Print_Red("Get DHT Error: " + error.args[0], __DHT22ErrorString)
        except Exception as e:
            MyPrint.Print_Red("Get DHT Module Error: " + error.args[0], __DHT22ErrorString)