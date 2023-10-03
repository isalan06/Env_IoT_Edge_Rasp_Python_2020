#!/usr/bin/python3
#MyDHT22Reader.py

import adafruit_dht
import board
import MyPrint


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

    def Start():
        global DHT22Data
        global dhtDevice

        try:
            dhtDevice = adafruit_dht.DHT22(board.D17)
            MyPrint.Print_Green("[DHT22 Info]Create DHT Device Success")
            DHT22Data.sDHT22Status="Running"
            DHT22Data.bDHT22DeviceExist = True
        except:
            dhtDevice = 0
            MyPrint.Print_Red("[DHT22 Info]Create DHT Device Fail")
            DHT22Data.sDHT22Status="Stop"
            DHT22Data.bDHT22DeviceExist = False

    def Read():
        global DHT22Data
        global dhtDevice

        try:
            if dhtDevice != 0:
                DHT22Data.temp_c = dhtDevice.temperature
                DHT22Data.humidity = dhtDevice.humidity
            else:
                MyPrint.Print_Red("[DHT22 Info]Get DHT Module did not exist")
        except RuntimeError as error:
            MyPrint.Print_Red("[DHT22 Info]Get DHT Error: " + error.args[0])
        except Exception as e:
            MyPrint.Print_Red("[DHT22 Info]Get DHT Module Error: " + error.args[0])