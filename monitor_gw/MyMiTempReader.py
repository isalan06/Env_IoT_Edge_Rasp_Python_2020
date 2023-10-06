#!/usr/bin/python3
#MyMiTempReader.py

from bluepy.btle import UUID, Peripheral
from bluepy import btle

import time
from datetime import datetime
import MyPrint
import threading
import argparse
import sys

MiInfoString = '[MI Info]'
MiErrorString = '[MI Info]'

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
                    MyPrint.Print_Red ('\t'+ '[MI Info]Get Sensors Address: %s' % (dev.addr))
                    singleFlag = True
                    for address_name in MiTemperData.mac_address_list:
                        if address_name == dev.addr:
                            singleFlag = False
                            break
                    if singleFlag:
                        MiTemperData.mac_address_list.append(dev.addr)

        if not dev.scanData:
            MyPrint.Print ('\t(no data)')
        

class Delegate_HandleReceivedData(btle.DefaultDelegate):
    
    def __init__(self, index):
        self.index=index
        btle.DefaultDelegate.__init__(self)
        MyPrint.Print("[Mi Info]Delegate initial Success-" + str(self.index))

    def handleNotification(self, cHandle, data):
            global MiTemperData

            if len(data) >= 3:
                data1 = data[0] #temperature Low
                data2 = data[1] #temperature High
                data3 = data[2] #humidity
                data4 = float(data2 * 256 + data1) / 100.0 #temperature
                data5 = int.from_bytes(data[3:5],byteorder='little') / 1000. #battery
                MyPrint.Print_White("Machine-" + str(self.index) + " => Get Temp:" + str(data4) + "C;   Humidity:" + str(data3) + "%RH; Voltage:" + str(data5), MiInfoString)
                if (self.index < MiTemperData.get_mi_device_number):
                    MiTemperData.get_mi_data_temp[self.index] = data4
                    MiTemperData.get_mi_data_humidity[self.index] = data3
                    MiTemperData.get_mi_data_battery[self.index] = data5
                    MiTemperData.get_mi_data_flag[self.index]=True
                    MiTemperData.get_mi_data_flag2[self.index]=True
                    if self.index == 0:
                        MiTemperData.get_mi_singledata_temp = data4
                        MiTemperData.get_mi_singledata_humidity = data3
                        MiTemperData.dtMiTimeoutTimer = time.time()
                        MiTemperData.dtCaptureMiTime = datetime.now()


class MyMiBLEDeivce():
    BLE_Connected=False
    p=None
    bRunning=False
    DoWorkThread = 0
    start_time=time.time()
    ReconnectIntervalSecond = 300#1800 # Capture MI Data interval time (sec)
    bFirstOneFlag=False

    start_time2=time.time()
    start_time3=time.time()
    GetBatteryValueIntervalSecond = 60

    def __init__(self, index, mac_address):
        self.index=index
        self.mac_address=mac_address

    def __connect(self):
        count = 5
        while (count > 0):
            count -= 1
            try:
                if self.p == None:
                    self.p = Peripheral(self.mac_address)
                    self.p.setDelegate(Delegate_HandleReceivedData(self.index))
                else:
                    self.p.connect()
                self.BLE_Connected = True
            except Exception as e:
                MyPrint.Print_Red("Machine-" + str(self.index) + " Connect Error. Retry count:" + str(count), MiErrorString)
                print (e)
                continue

            try:
                if self.bFirstOneFlag == False:
                    se10=self.p.getServiceByUUID('ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6')
                    ch10=se10.getCharacteristics('ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6')
                    ccc_desc = ch10[0].getDescriptors(forUUID=0x2902)[0]
                    ccc_desc.write(b"\x02")
                    self.bFirstOneFlag = True
                    MyPrint.Print_Green("Machine-" + str(self.index) + " Set Notification Success", MiInfoString)
                    return True
            except:
                MyPrint.Print_Red("Machine-" + str(self.index) + " Set Notification Error", MiErrorString)
                return False
            time.sleep(1.0)
            
        return False

    def Connect(self):
        MyPrint.Print("[Mi Info]Start To Connect BLE-" + str(self.index) + " - " +self.mac_address)
        try:
            result = self.__connect()
            if result:
                MyPrint.Print_Green("Machine-" + str(self.index) + " Connect Success", MiInfoString)
            else:
                self.BLE_Connected = False
                MyPrint.Print_Red("Machine-" + str(self.index) + " Connect Error", MiErrorString)
         
        except:
            self.BLE_Connected = False
            MyPrint.Print_Red("Machine-" + str(self.index) + " Connect Error", MiErrorString)

    def Run(self):
        try:
            self.bRunning = True
            self.DoWorkThread = threading.Thread(target=self.DoWork)
            self.DoWorkThread.start()
            MyPrint.Print_Green("Machine-" + str(self.index) + " Run Threading Success", MiInfoString)
        except:
            MyPrint.Print_Red("Machine-" + str(self.index) + " Run Threading Fail", MiErrorString)
        finally:
            pass
            

    def DoWork(self):
        global get_mi_data_battery

        waitForNotificationsValue = 3.0

        while self.bRunning:
            if (self.BLE_Connected & self.bRunning):
                try:
                    self.p.waitForNotifications(waitForNotificationsValue)
                    MyPrint.Print_Green("Machine-" + str(self.index) + " - Wait For Notification Success", MiInfoString)
                except:
                    self.BLE_Connected = False
                    MyPrint.Print_Red("Machine-" + str(self.index) + " - Wait For Notification Error", MiErrorString)
            else:
                timer = time.time()-self.start_time3
                if ((int(timer)>self.ReconnectIntervalSecond) or (timer < 0)):
                    self.start_time3=time.time()
                    self.Connect()

            time.sleep(waitForNotificationsValue)

    def Disconnect(self):
        if self.BLE_Connected == True:
            self.start_time3=time.time()
            self.BLE_Connected = False
            try:
                self.p.disconnect()
                MyPrint.Print_Green("Machine-" + str(self.index) + " - Disconnect Success", MiInfoString)
            except:
                self.p=None
                MyPrint.Print_Red("Machine-" + str(self.index) + " - Disconnect Fail", MiErrorString)
    
    def Close(self):
        self.bRunning = False
        if self.BLE_Connected == True:
            try:
                self.p.disconnect()
                MyPrint.Print("Machine-" + str(self.index) + " - Disconnect Success", MiInfoString)
            except:
                self.p=None
                MyPrint.Print("Machine-" + str(self.index) + " - Disconnect Fail", MiErrorString)

class BLEDeviceForMi():
    
    bBLEDeviceExist = False
    bCheckBLEDeivce = False
    bExecuteConnect = False
    bExecuteStop = False
    bRunning = False
    DoWorkThread = 0
    myBleDevice=[]
    

    def __init__(self, bScanBLE):
        self.bScanBLE = bScanBLE
        self.bRunning = True
        self.DoWorkThread = threading.Thread(target=self.DoWork)
        self.DoWorkThread.start()

    def Start(self):
        self.bExecuteConnect = True

    def Stop(self):
        self.bExecuteStop = True

    def DoWork(self):
        global MiTemperData

        while self.bRunning:

            #Connect
            #region
            if self.bExecuteConnect:
                self.bExecuteConnect = False

                # Scan BLE
                #region Scan BLE

                if self.bScanBLE:
                    parser = argparse.ArgumentParser()
                    parser.add_argument('-i', '--hci', action='store', type=int, default=0,
                        help='Interface number for scan')
                    parser.add_argument('-t', '--timeout', action='store', type=int, default=4,
                        help='Scan delay, 0 for continuous')
                    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128,
                        help='dBm value for filtering far devices')
                    parser.add_argument('-d', '--discover', action='store_true',
                        help='Connect and discover service to scanned devices')
                    parser.add_argument('-a', '--all', action='store_true',
                        help='Display duplicate adv responses, by default show new + updated')
                    parser.add_argument('-n', '--new', action='store_true',
                        help='Display only new adv responses, by default show new + updated')
                    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase output verbosity')
                    arg = parser.parse_args(sys.argv[1:])

                    btle.Debugging = arg.verbose

                    scanner = btle.Scanner(arg.hci).withDelegate(Delegate_ScanMiDevice(arg))

                    MyPrint.Print_Cyan ("Scanning for devices...", MiInfoString)
                    #devices = scanner.scan(arg.timeout)
                    try:
                        devices = scanner.scan(10)
                    except:
                        MyPrint.Print_Red("Scanning for devices happen error", MiErrorString)


                #endregion

                # Connect to BLE Device
                #region Connect to BLE Device

                length = len(MiTemperData.mac_address_list)

                if length > 0:
                    self.bBLEDeviceExist = True

                if self.bBLEDeviceExist:
                    MyPrint.Print("[MI Info]List of Mac Address: Number=>" + str(length))
                    MyPrint.Print(MiTemperData.mac_address_list)

                    for index in range(length):
                        _device = MyMiBLEDeivce(index, MiTemperData.mac_address_list[index])
                        _device.Connect()
                        _device.Run()
                        self.myBleDevice.append(_device)
                        MiTemperData.get_mi_data_flag.append(False)
                        MiTemperData.get_mi_data_flag2.append(False)
                        MiTemperData.get_mi_data_temp.append(0.0)
                        MiTemperData.get_mi_data_humidity.append(0)
                        MiTemperData.get_mi_data_battery.append(0)
                        MiTemperData.get_mi_device_number = MiTemperData.get_mi_device_number + 1

                        time.sleep(1.0)

                    #get_mi_device_number = length
                    MyPrint.Print_Yellow("List of Mac Address: Number=>" + str(MiTemperData.get_mi_device_number), MiInfoString)

                else:
                    MyPrint.Print("[MI Info]There is no BLE Device")

                #endregion
            #endregion

            # Disconnect
            #region
            length = len(MiTemperData.mac_address_list)
            if length > 0:
                for index in range(length):
                    if MiTemperData.get_mi_data_flag2[index] == True:
                        MiTemperData.get_mi_data_flag2[index] = False
                        self.myBleDevice[index].Disconnect()

            #endregion

            # Close
            #region

            if self.bExecuteStop:
                self.bExecuteStop = False
                for index in range(length):
                    self.myBleDevice[index].Close()
                self.bRunning = False

            #endregion

            time.sleep(0.5)
