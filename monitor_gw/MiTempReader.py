#!/usr/bin/python3
#MiTempReader.py

from bluepy.btle import UUID, Peripheral
from bluepy import btle

import time
from datetime import datetime


class MiTemperDataDto:
    get_mi_device_number = 0
    mac_address_list = []
    get_mi_data_flag = []
    get_mi_data_flag2 = []
    get_mi_data_temp = []
    get_mi_data_humidity = []
    get_mi_data_battery = []
    get_mi_singledata_temp = 0
    get_mi_singledata_humidity = 0
    dtMiTimeoutTimer = time.time()
    dtStartTime = datetime.now()
    dtCaptureMiTime = datetime.now()
    update_mi_data_temp = 0
    update_mi_data_humidity = 0
    
    def __init__(self):
        pass


MiTemperData = MiTemperDataDto()

class Delegate_ScanMiDevice(btle.DefaultDelegate):

    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleDiscovery(self, dev, isNewDev, isNewData):
        global MiTemperData

        if isNewDev:
            status = "new"
        elif isNewData:
            if self.opts.new:
                return
            status = "update"
        else:
            if not self.opts.all:
                return
            status = "old"

        if dev.rssi < self.opts.sensitivity:
            return

        for (sdid, desc, val) in dev.getScanData():
            if(desc == 'Complete Local Name'):
                if(val == 'LYWSD03MMC'):
                    print ('\t' + ANSI_RED + 'Get Sensors Address: %s' % (dev.addr) + ANSI_OFF)
                    MiTemperData.mac_address_list.append(dev.addr)

        if not dev.scanData:
            print ('\t(no data)')
        print

class Delegate_HandleReceivedData(btle.DefaultDelegate):
    
    def __init__(self, index):
        self.index=index
        btle.DefaultDelegate.__init__(self)
        print("Delegate initial Success-" + str(self.index))

    def handleNotification(self, cHandle, data):
            global get_mi_device_number
            global get_mi_data_flag
            global get_mi_data_flag2
            global get_mi_data_temp
            global get_mi_data_humidity
            global get_mi_singledata_temp
            global get_mi_singledata_humidity
            global dtMiTimeoutTimer
            global dtCaptureMiTime
            #print(data)
            if len(data) >= 3:
                data1 = data[0]
                data2 = data[1]
                data3 = data[2]
                data4 = float(data2 * 256 + data1) / 100.0
                data5 = int.from_bytes(data[3:5],byteorder='little') / 1000.
                #print("Get Notification (" + str(get_mi_device_number) + ")")
                print("  Machine-" + str(self.index) + " => Get Temp:" + str(data4) + "C;   Humidity:" + str(data3) + "%RH; Voltage:" + str(data5))
                if (self.index < get_mi_device_number):
                    get_mi_data_temp[self.index] = data4
                    get_mi_data_humidity[self.index] = data3
                    get_mi_data_battery[self.index] = data5
                    get_mi_data_flag[self.index]=True
                    get_mi_data_flag2[self.index]=True
                    if self.index == 0:
                        get_mi_singledata_temp = data4
                        get_mi_singledata_humidity = data3
                        dtMiTimeoutTimer = time.time()
                        dtCaptureMiTime = datetime.now()



class MiTempReader:
    def __init__(self):
        pass