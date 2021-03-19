#!/usr/bin/python3
import argparse
import binascii
import os
import cv2
import smbus
import math
import time
import board
import adafruit_dht
import json
import requests
from datetime import datetime
import ssl
from Adafruit_AMG88xx import Adafruit_AMG88xx
import threading

import picamera

import MyParameter
import MyCamera

import sys
import struct
from bluepy.btle import UUID, Peripheral
from bluepy import btle

import socket
import uuid
import psutil

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image

sSoftwareVersion='1.0.5.6'

get_mi_device_number = 0
mac_address_list = []
get_mi_data_flag = []
get_mi_data_flag2 = []
get_mi_data_temp = []
get_mi_data_humidity = []
get_mi_data_battery = []

hostname = ''
local_mac_address = ''
hostip = ''


if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'

def get_mac_address():
    #mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    #return ":".join([mac[e:e+2] for e in range(0,11,2)])
    mac = '000000000000'
    nics = psutil.net_if_addrs()['eth0']
    for interface in nics:
        if interface.family == 17:
            mac = interface.address.replace(':','')
    return mac

# BLE Program
#region

def dump_services(dev):
    services = sorted(dev.services, key=lambda s: s.hndStart)
    for s in services:
        print ("\t%04x: %s" % (s.hndStart, s))
        if s.hndStart == s.hndEnd:
            continue
        chars = s.getCharacteristics()
        for i, c in enumerate(chars):
            props = c.propertiesToString()
            h = c.getHandle()
            if 'READ' in props:
                val = c.read()
                if c.uuid == btle.AssignedNumbers.device_name:
                    string = ANSI_CYAN + '\'' + \
                        val.decode('utf-8') + '\'' + ANSI_OFF
                elif c.uuid == btle.AssignedNumbers.device_information:
                    string = repr(val)
                else:
                    string = '<s' + binascii.b2a_hex(val).decode('utf-8') + '>'
            else:
                string = ''
            print ("\t%04x:    %-59s %-12s %s" % (h, c, props, string))

            while True:
                h += 1
                if h > s.hndEnd or (i < len(chars) - 1 and h >= chars[i + 1].getHandle() - 1):
                    break
                try:
                    val = dev.readCharacteristic(h)
                    print ("\t%04x:     <%s>" %
                           (h, binascii.b2a_hex(val).decode('utf-8')))
                except btle.BTLEException:
                    break


class ScanPrint(btle.DefaultDelegate):

    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleDiscovery(self, dev, isNewDev, isNewData):
        global mac_address_list

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
                    mac_address_list.append(dev.addr)

        if not dev.scanData:
            print ('\t(no data)')
        print

class MyDelegate(btle.DefaultDelegate):
    
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

class MyTest():
    BLE_Connected=False
    p=None
    bRunning=False
    DoWorkThread = 0
    start_time=time.time()
    ReconnectIntervalSecond = 1800
    bFirstOneFlag=False

    start_time2=time.time()
    start_time3=time.time()
    GetBatteryValueIntervalSecond = 30

    def __init__(self, index, mac_address):
        self.index=index
        self.mac_address=mac_address

    def Connect(self):
        print("Start To Connect BLE-" + str(self.index))
        try:
            self.p = Peripheral(self.mac_address)
            self.p.setDelegate(MyDelegate(self.index))
            self.BLE_Connected = True

            try:
                if self.bFirstOneFlag == False:
                    se10=self.p.getServiceByUUID('ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6')
                    ch10=se10.getCharacteristics('ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6')
                    ccc_desc = ch10[0].getDescriptors(forUUID=0x2902)[0]
                    ccc_desc.write(b"\x02")
                    self.bFirstOneFlag = True
            except:
                print("Machine-" + str(self.index) + " Set Notification Error")
         
        except:
            self.BLE_Connected = False
            print("Machine-" + str(self.index) + " Connect Error")

    def Run(self):
        try:
            self.bRunning = True
            self.DoWorkThread = threading.Thread(target=self.DoWork)
            self.DoWorkThread.start()
        except:
            print("Machine-" + str(self.index) + " Run Threading Fail")
        finally:
            print("Machine-" + str(self.index) + " Run Threading Success")

    def DoWork(self):
        global get_mi_data_battery
        while self.bRunning:
            if (self.BLE_Connected & self.bRunning):
                try:
                    self.p.waitForNotifications(0.5)
                except:
                    self.BLE_Connected = False
                    print("Machine-" + str(self.index) + " - Wait For Notification Error")
            else:
                timer = time.time()-self.start_time3
                if ((int(timer)>self.ReconnectIntervalSecond) or (timer < 0)):
                    self.start_time3=time.time()
                    self.Connect()
            time.sleep(0.5)

    def Disconnect(self):
        if self.BLE_Connected == True:
            self.start_time3=time.time()
            self.BLE_Connected = False
            try:
                self.p.disconnect()
                print(ANSI_GREEN + "@@@@Machine-" + str(self.index) + " - Disconnect Success" + ANSI_OFF)
            except:
                self.p=None
                print(ANSI_RED + "@@@@Machine-" + str(self.index) + " - Disconnect Fail" + ANSI_OFF)
    
    def Close(self):
        self.bRunning = False
        if self.BLE_Connected == True:
            try:
                self.p.disconnect()
                print("Machine-" + str(self.index) + " - Disconnect Success")
            except:
                self.p=None
                print("Machine-" + str(self.index) + " - Disconnect Fail")

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
        global mac_address_list
        global get_mi_device_number
        global get_mi_data_flag
        global get_mi_data_flag2
        global get_mi_data_temp
        global get_mi_data_humidity
        global get_mi_data_battery

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

                    scanner = btle.Scanner(arg.hci).withDelegate(ScanPrint(arg))

                    print (ANSI_RED + "Scanning for devices..." + ANSI_OFF)
                    #devices = scanner.scan(arg.timeout)
                    try:
                        devices = scanner.scan(20)
                    except:
                        print("Scanning for devices happen error")


                #endregion

                # Connect to BLE Device
                #region Connect to BLE Device

                length = len(mac_address_list)

                if length > 0:
                    self.bBLEDeviceExist = True

                if self.bBLEDeviceExist:
                    print("List of Mac Address: Number=>" + str(length))
                    print(mac_address_list)

                    for index in range(length):
                        _device = MyTest(index, mac_address_list[index])
                        _device.Connect()
                        _device.Run()
                        self.myBleDevice.append(_device)
                        get_mi_data_flag.append(False)
                        get_mi_data_flag2.append(False)
                        get_mi_data_temp.append(0.0)
                        get_mi_data_humidity.append(0)
                        get_mi_data_battery.append(0)
                        get_mi_device_number = get_mi_device_number + 1

                        time.sleep(1.0)

                    #get_mi_device_number = length
                    print(ANSI_YELLOW + "List of Mac Address: Number=>" + str(get_mi_device_number) + ANSI_OFF)

                else:
                    print("There is no BLE Device")

                #endregion
            #endregion

            # Disconnect
            #region
            length = len(mac_address_list)
            if length > 0:
                for index in range(length):
                    if get_mi_data_flag2[index] == True:
                        get_mi_data_flag2[index] = False
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

#endregion

#Flag
bRunning = True
bGetData = False
bNetConnected = False
bRebootTrigger = False
bCameraUsed = False
bRecordVibration = False

#Manual Flag
bManualCaptureImage = False
bManualCaptureVideo = False
bManualVibrationStatus = False
bManualFireDetectStatus = False

#Alarm Status
sVibrationStatus = "Normal"
sVibrationStatus_Keep = "Normal"
sFireDetectStatus = "Normal"

#Component Status
sDHT22Status = "Stop"
sAccelGaugeStatus = "Stop"
sThermalStatus = "Stop"

#Vibration Attribute
gyro_xout = 0
gyro_yout = 0
gyro_zout = 0
gyro_xout_scaled = 0
gyro_yout_scaled = 0
gyro_zout_scaled = 0
accel_xout = 0
accel_yout = 0
accel_zout = 0
accel_xout_scaled = 0
accel_yout_scaled = 0
accel_zout_scaled = 0
x_rotation = 0
y_rotation = 0

#AMG8833 Attribute
thermalpixels= []
thermalmaxValue = 0.0
thermalminValue = 0.0

#DHT Attribute
temp_c=0.0
humidity=0

#Vibration Attribute
vib_bus = smbus.SMBus(1)
vib_address = 0x68

#Vibration Power Management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

#Vibration - Now make the 6050 up as it starts in sleep mode
vib_bus.write_byte_data(vib_address, power_mgmt_1, 0)

#Vibration Function
#region Vibration Function
def read_byte(adr):
    return vib_bus.read_byte_data(vib_address, adr)

def read_word(adr):
    high = vib_bus.read_byte_data(vib_address, adr)
    low = vib_bus.read_byte_data(vib_address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if(val > 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)

def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

#endregion

#Get Sensors Data
#region Get Sensors Data
def GetSensorsData():

    global bRunning
    global bGetData
    global bNetConnected

    #DHT Attribute
    global temp_c
    global humidity

    #Vibration Attribute
    global gyro_xout
    global gyro_yout
    global gyro_zout
    global gyro_xout_scaled
    global gyro_yout_scaled
    global gyro_zout_scaled
    global accel_xout
    global accel_yout
    global accel_zout
    global accel_xout_scaled
    global accel_yout_scaled
    global accel_zout_scaled
    global x_rotation
    global y_rotation

    #Alarm Status
    global sVibrationStatus
    global sFireDetectStatus
    global sVibrationStatus_Keep

    #component Status
    global sDHT22Status
    global sAccelGaugeStatus
    global sThermalStatus

    #AMG8833 Attribute
    global thermalpixels
    global thermalmaxValue
    global thermalminValue

    #Record Vibration
    global bRecordVibration
    calCount_RecordVibration = 0
    RecordVibrationData = {}
    tKeepVibrationStatusTimer = time.time()
    iKeepVibrationStatus_IntervalTime = 5.0

    #Vibration
    bVibration_FirstFlag = False
    gyro_xout_pre = 0.0
    gyro_yout_pre = 0.0
    gyro_zout_pre = 0.0

    #Capture Delay
    tStartTime_DHT22 = time.time()
    tStartTime_Thermal = time.time()
    fIntervalTime_Thermal = 1.0
    tEndTime = time.time()
    tStartTime_ShowInformation = time.time()
    fIntervalTime_ShowInformation = 10.0

    print("Get Local Sensors Thread Start")

    # DHT22 Attribute
    dhtDevice = 0
    try:
        dhtDevice = adafruit_dht.DHT22(board.D17)
        print(ANSI_GREEN + "Create DHT Device Success" + ANSI_OFF)
        sDHT22Status="Running"
    except:
        dhtDevice = 0
        print(ANSI_RED + "Create DHT Device Fail" + ANSI_OFF)
        sDHT22Status="Stop"

    #AMG8833 Attribute
    thermalImage = 0
    try:
        thermalImage = Adafruit_AMG88xx()
        print(ANSI_GREEN + "Connect to Theraml Camera Success" + ANSI_OFF)
        sThermalStatus = "Running"
    except:
        thermalImage = 0
        print(ANSI_RED + "Connect to Theraml Camera Fail" + ANSI_OFF)
        sThermalStatus = "Stop"

    while bRunning:
        tEndTime = time.time()

        if (tEndTime - tStartTime_ShowInformation) >= fIntervalTime_ShowInformation:
            tStartTime_ShowInformation = time.time()
            print(ANSI_YELLOW + "Capture Sensors---------------------------------------------------")
            print("     Temp: {:.1f}C Humidity: {}%".format(temp_c, humidity))
            print("     Get G Sensors Success: " + sVibrationStatus)
            print("     Get ThermalPixels Success: " + sFireDetectStatus)
            print("------------------------------------------------------------------" + ANSI_OFF)

        #DHT22
        try:
            if dhtDevice != 0:
                checkvalue = tEndTime - tStartTime_DHT22
                if (checkvalue >= MyParameter.SensorsFValue) or (checkvalue < 0):
                    tStartTime_DHT22 = time.time()
                    temp_c = dhtDevice.temperature
                    humidity = dhtDevice.humidity
        except RuntimeError as error:
            print("Get DHT Error: " + error.args[0])

        #Vibration Status Return Normal Check
        if sVibrationStatus == "Normal":
            if sVibrationStatus_Keep != "Normal":
                intervaltime = time.time() - tKeepVibrationStatusTimer
                if (intervaltime >= iKeepVibrationStatus_IntervalTime) or (intervaltime < 0):
                    sVibrationStatus_Keep = "Normal"

        #Vibration
        try:
            gyro_xout = read_word_2c(0x43)
            gyro_yout = read_word_2c(0x45)
            gyro_zout = read_word_2c(0x47)
            gyro_xout_scaled = gyro_xout / 131
            gyro_yout_scaled = gyro_yout / 131
            gyro_zout_scaled = gyro_zout / 131
            accel_xout = read_word_2c(0x3b)
            accel_yout = read_word_2c(0x3d)
            accel_zout = read_word_2c(0x3f)
            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0
            x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            y_rotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

            gyro_xout_amp = 0.0
            gyro_yout_amp = 0.0
            gyro_zout_amp = 0.0

            if bVibration_FirstFlag == True :
                gyro_xout_amp = gyro_xout_scaled - gyro_xout_pre
                gyro_yout_amp = gyro_yout_scaled - gyro_yout_pre
                gyro_zout_amp = gyro_zout_scaled - gyro_zout_pre
            gyro_xout_pre = gyro_xout_scaled
            gyro_yout_pre = gyro_yout_scaled
            gyro_zout_pre = gyro_zout_scaled
            bVibration_FirstFlag = True

            if (abs(gyro_xout_amp) > MyParameter.VibrationAlarmValue) or (abs(gyro_yout_amp) > MyParameter.VibrationAlarmValue) or (abs(gyro_zout_amp) > MyParameter.VibrationAlarmValue):
                sVibrationStatus = "Alarm"
                sVibrationStatus_Keep = "Alarm"
                tKeepVibrationStatusTimer = time.time()
            elif (abs(gyro_xout_amp) > MyParameter.VibrationWarningValue) or (abs(gyro_yout_amp) > MyParameter.VibrationWarningValue) or (abs(gyro_zout_amp) > MyParameter.VibrationWarningValue):
                sVibrationStatus = "Warning"
                if sVibrationStatus_Keep == "Normal":
                    sVibrationStatus_Keep = "Alarm"
                tKeepVibrationStatusTimer = time.time()
            else:
                sVibrationStatus = "Normal"
            if bRecordVibration:
                if calCount_RecordVibration == 0:
                    RecordVibrationData = {}
                    RecordVibrationData["Machine ID"]=local_mac_address
                    RecordVibrationData["Command"]="UpdateRecordVibration"
                    RecordVibrationData["Data"] = []

                datalist = {}
                datalist['Gx']=gyro_xout_scaled
                datalist['Gy']=gyro_yout_scaled
                datalist['Gz']=gyro_zout_scaled
                datalist['Ax']=accel_xout_scaled
                datalist['Ay']=accel_yout_scaled
                datalist['Az']=accel_zout_scaled
                RecordVibrationData["Data"].append(datalist)

                calCount_RecordVibration = calCount_RecordVibration + 1
                if calCount_RecordVibration >= 100:
                    bRecordVibration = False
                    calCount_RecordVibration = 0
                    TransferJSONData=json.dumps(RecordVibrationData)
                    try:
                        auth=('token', 'example')
                        ssl._create_default_https_context = ssl._create_unverified_context
                        headers = {'Content-Type': 'application/json'}
                        r = requests.post('https://script.google.com/macros/s/AKfycbyaqQfJagU3KR5ccgIfWkD99dLLtn-NQJbwNJ9siPdVU7VJsoA/exec',headers=headers, data=TransferJSONData, auth=auth)
                        print(ANSI_GREEN + "--Update Record Vibration Success" + ANSI_OFF)
                    except BaseException as error:
                        print(ANSI_RED + "--Update Record Vibration Failure" + ANSI_OFF)

            sAccelGaugeStatus = "Running"
        except:
            print("Get G Sensor Failure")
            sAccelGaugeStatus = "Stop"
            

        #Thermal Image
        try:
            if thermalImage != 0:
                checkvalue = tEndTime - tStartTime_Thermal
                if (checkvalue >= fIntervalTime_Thermal) or (checkvalue < 0):
                    tStartTime_Thermal = time.time()
                    thermalpixels = thermalImage.readPixels()

                    fireAlarmCount=0
                    fireWarningCount=0
                    bFirstFlag = False
                    for i in thermalpixels:
                        if i > MyParameter.FireAlarmTempValue:
                            fireAlarmCount += 1
                        elif i > MyParameter.FireWarningTempValue:
                            fireWarningCount += 1
                        if not bFirstFlag:
                            bFirstFlag=True
                            thermalmaxValue = i
                            thermalminValue = i
                        else:
                            if i > thermalmaxValue:
                                thermalmaxValue=i
                            if i < thermalminValue:
                                thermalminValue=i

                    if fireAlarmCount > MyParameter.FireAlarmCountValue:
                        sFireDetectStatus="Alarm"
                    elif fireWarningCount > MyParameter.FireWarningCountValue:
                        sFireDetectStatus="Warning"
                    else:
                        sFireDetectStatus="Normal"
                    #print("Get ThermalPixels Success: " + sFireDetectStatus)
        except:
            print("Get TermalPixels Failure")
            

        bGetData = True

        # Delay for getting Vibration Sensors (0.1 sec)
        time.sleep(0.1)
        #time.sleep(SensorsFValue)
#endregion

#Update Local Sensors Information
#region Update Local Sensors Information

def UpdateLocalSensorsInformation():

    global get_mi_device_number
    global get_mi_data_flag
    global get_mi_data_flag2
    global get_mi_data_temp
    global get_mi_data_humidity
    global get_mi_data_battery
    global mac_address_list


    global bRunning
    global bGetData
    global bNetConnected

    global local_mac_address
    global hostip

    global sDHT22Status
    global sAccelGaugeStatus
    global sThermalStatus
    

    #DHT Attribute
    global temp_c
    global humidity

    #Vibration Attribute
    global gyro_xout
    global gyro_yout
    global gyro_zout
    global gyro_xout_scaled
    global gyro_yout_scaled
    global gyro_zout_scaled
    global accel_xout
    global accel_yout
    global accel_zout
    global accel_xout_scaled
    global accel_yout_scaled
    global accel_zout_scaled
    global x_rotation
    global y_rotation

    #AMG8833 Attribute
    global thermalpixels

    global sVibrationStatus_Keep


    #print("Update Sensors Informatnio Start")
    while bRunning:
        try:
            time.sleep(MyParameter.UpdateFValue)
        except:
            time.sleep(10.0)
        if bGetData: # & bNetConnected:
            bGetData = False

            try:
                #JSON
                SetKey="Machine"
                SetValue="IoT Edge"
                InformationData = {}
                InformationData[SetKey]=SetValue
                InformationData["Machine ID"]=local_mac_address
                InformationData["SoftwareVersion"]=sSoftwareVersion
                InformationData["CameraSWVersion"]=MyCamera.sSoftwareVersion
                InformationData["ParameterSWVersion"]=MyParameter.sSoftwareVersion
                InformationData["Comm Type"]="Ethernet"
                InformationData["VibrationStatus"]=sVibrationStatus_Keep
                InformationData["FireDetectStatus"]=sFireDetectStatus
                InformationData["DHT22Status"]=sDHT22Status
                InformationData["AccelGaugeStatus"]=sAccelGaugeStatus
                InformationData["ThermalStatus"]=sThermalStatus
                InformationData["Gateway Time"]=datetime.now().strftime("%Y%m%d%H%M%S")	
                InformationData["Command"]="UpdateStatus"
                InformationData["MachineIP"]=hostip
                SetKey="Parameter"
                InformationData[SetKey]={}
                InformationData[SetKey]['VibrationWarningValue']=MyParameter.VibrationWarningValue
                InformationData[SetKey]['VibrationAlarmValue']=MyParameter.VibrationAlarmValue
                InformationData[SetKey]['FireWarningTempValue']=MyParameter.FireWarningTempValue
                InformationData[SetKey]['FireWarningCountValue']=MyParameter.FireWarningCountValue
                InformationData[SetKey]['FireAlarmTempValue']=MyParameter.FireAlarmTempValue
                InformationData[SetKey]['FireAlarmCountValue']=MyParameter.FireAlarmCountValue
                InformationData[SetKey]['CapturePictureRH']=MyParameter.CapturePictureRH
                InformationData[SetKey]['CapturePictureRV']=MyParameter.CapturePictureRV
                InformationData[SetKey]['CaptureVideoSecond']=MyParameter.CaptureVideoSecond
                InformationData[SetKey]['SensorsFValue']=MyParameter.SensorsFValue
                InformationData[SetKey]['CameraFValue']=MyParameter.CameraFValue
                InformationData[SetKey]['UpdateFValue']=MyParameter.UpdateFValue
                InformationData[SetKey]['PhotoFolderID']=MyParameter.PhotoFolderID
                InformationData[SetKey]['VideoFolderID']=MyParameter.VideoFolderID

                SetKey="Data"
                InformationData[SetKey]={}
                SetKey2="Temp"
                SetKey3="Data"
                InformationData[SetKey][SetKey2]={}
                InformationData[SetKey][SetKey2]["Count"]=1
                InformationData[SetKey][SetKey2][SetKey3]=[]
                templist = {}
                templist["ID"]=1
                templist["Type"]="Local"
                templist["Unit"]="C"
                templist["Address"]="NA"
                templist["Value"]=temp_c
                InformationData[SetKey][SetKey2][SetKey3].append(templist)
                
                SetKey2="Humidity"
                InformationData[SetKey][SetKey2]={}
                InformationData[SetKey][SetKey2]["Count"]=1
                InformationData[SetKey][SetKey2][SetKey3]=[]
                humiditylist = {}
                humiditylist["ID"]=1
                humiditylist["Type"]="Local"
                humiditylist["Unit"]="%RH"
                humiditylist["Value"]=humidity
                InformationData[SetKey][SetKey2][SetKey3].append(humiditylist)

                print("\t" + ANSI_YELLOW + "Check MI Device Number: " + str(get_mi_device_number) + ANSI_OFF)
                SetKey2="MiTempHumidity"
                InformationData[SetKey][SetKey2]={}
                InformationData[SetKey][SetKey2]["Count"]=0
                InformationData[SetKey][SetKey2][SetKey3]=[]
                if (get_mi_device_number > 0):
                    print("\t" + ANSI_YELLOW + "Create MI Device JSON" + ANSI_OFF)
                    Count = 0
                
                    for index in range(get_mi_device_number):
                        if get_mi_data_flag[index]:
                            get_mi_data_flag[index] = False
                            Count = Count + 1
                            InformationData[SetKey][SetKey2]["Count"]=Count

                            mithlist = {}
                            mithlist["ID"]=mac_address_list[index]
                            mithlist["Type"]="MI Remote"
                            mithlist["TUnit"]="C"
                            mithlist["TValue"]=get_mi_data_temp[index]
                            mithlist["HUnit"]="%RH"
                            mithlist["HValue"]=get_mi_data_humidity[index]
                            mithlist["BUnit"]="%"
                            mithlist["BValue"]=get_mi_data_battery[index]

                            InformationData[SetKey][SetKey2][SetKey3].append(mithlist)

            
                SetKey2="Vibration"
                InformationData[SetKey][SetKey2]={}
                InformationData[SetKey][SetKey2]["Count"]=1
                InformationData[SetKey][SetKey2][SetKey3]=[]
                VibrationList={}
                VibrationList["ID"]=1
                VibrationList["Type"]="Local"
                VibrationList["GyroUnit"]="DegreePerSecond"
                VibrationList["GyroX"]=gyro_xout
                VibrationList["GyroXScaled"]=gyro_xout_scaled
                VibrationList["GyroY"]=gyro_yout
                VibrationList["GyroYScaled"]=gyro_yout_scaled
                VibrationList["GyroZ"]=gyro_zout
                VibrationList["GyroZScaled"]=gyro_zout_scaled
                VibrationList["AccelUnit"]="g"
                VibrationList["AccelX"]=accel_xout
                VibrationList["AccelXScaled"]=accel_xout_scaled
                VibrationList["AccelY"]=accel_yout
                VibrationList["AccelYScaled"]=accel_yout_scaled
                VibrationList["AccelZ"]=accel_zout
                VibrationList["AccelZScaled"]=accel_zout_scaled
                VibrationList["RotationUnit"]="Degree"
                VibrationList["RotationX"]=x_rotation
                VibrationList["RotationY"]=y_rotation
                InformationData[SetKey][SetKey2][SetKey3].append(VibrationList)

                SetKey2="ThermalCamera"
                InformationData[SetKey][SetKey2]={}
                InformationData[SetKey][SetKey2]["Count"]=1
                InformationData[SetKey][SetKey2][SetKey3]=[]
                thermalDataLength=len(thermalpixels)
                ThermalDataList={}
                ThermalDataList["ID"]=1
                ThermalDataList["Type"]="Local"
                ThermalDataList["Unit"]="C"
                ThermalDataList["Length"]=thermalDataLength
                ThermalDataList["Value"]=[]
                setIDIndex=1
                for thermalpoint in thermalpixels:
                    ThermalDataValue={}
                    ThermalDataValue["ID"]=setIDIndex
                    ThermalDataValue["Value"]=thermalpoint
                    setIDIndex = setIDIndex + 1
                    ThermalDataList["Value"].append(ThermalDataValue)
                InformationData[SetKey][SetKey2][SetKey3].append(ThermalDataList)

                TransferJSONData=json.dumps(InformationData)
                #print(TransferJSONData)
                print(ANSI_GREEN + "Create JSON File Success" + ANSI_OFF) 
            except:
                print(ANSI_RED + "Create JSON File Failure" + ANSI_OFF) 

            try:
                auth=('token', 'example')
                ssl._create_default_https_context = ssl._create_unverified_context
                headers = {'Content-Type': 'application/json'}
                #r = requests.post('https://script.google.com/macros/s/AKfycbwOx-ypSoziN9f9__rit-_J3bjYP8sSOPoIfzo1rqi3QRIl-DQ/exec',headers=headers, data=TransferJSONData, auth=auth)
                r = requests.post('https://script.google.com/macros/s/AKfycbyaqQfJagU3KR5ccgIfWkD99dLLtn-NQJbwNJ9siPdVU7VJsoA/exec',headers=headers, data=TransferJSONData, auth=auth)
                print("\033[1;32mUpdate Sensors Information Success\033[0m")
            except BaseException as error:
                bNetConnected = False
                print("\033[1;31mUpdate Sensors Information Failure\033[0m")

#endregion

#Trigger Alarm to Cloud
#region

def TriggerAlarmToCloud():
    try:
        url = "http://122.116.123.236/Antiquities/API/WebService1.asmx/IotGWNotify"

        payload="{\"machineId\":\"" + local_mac_address + "\"}"
        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", url, headers=headers, data=payload)
        print(ANSI_YELLOW + "--Trigger Alarm To Cloud Result: " + response.text + ANSI_OFF)
    except:
        print(ANSI_RED + "--Trigger Alarm To Cloud Happen Error!" + ANSI_OFF)

#endregion



#Get Command From Cloud
#region Get Command From Cloud
def GetCommandFromCloud():
    global bRunning
    global bNetConnected
    global bRebootTrigger
    global bRecordVibration

    #Parameter
    global VibrationWarningValue
    global VibrationAlarmValue
    global FireWarningTempValue
    global FireWarningCountValue
    global FireAlarmTempValue
    global FireAlarmCountValue
    global CapturePictureRH
    global CapturePictureRV
    global CaptureVideoSecond
    global SensorsFValue
    global CameraFValue
    global UpdateFValue
    global PhotoFolderID
    global VideoFolderID

    global bCameraUsed
    global ftp

    global sVibrationStatus
    global sFireDetectStatus
    global sVibrationStatus_Keep

    global local_mac_address

    #Manual Flag
    global bManualCaptureImage
    global bManualCaptureVideo
    global bManualVibrationStatus
    global bManualFireDetectStatus

    #flag
    bCaptureImage = False
    bCaptureVideo = False
    bVibrationStatus = False
    bFireDetectStatus = False

    _Command = ""

    #print("Get Command From Cloud")
    
    while bRunning:

        #url = "https://script.google.com/macros/s/AKfycbwOx-ypSoziN9f9__rit-_J3bjYP8sSOPoIfzo1rqi3QRIl-DQ/exec"
        url = "https://script.google.com/macros/s/AKfycbyaqQfJagU3KR5ccgIfWkD99dLLtn-NQJbwNJ9siPdVU7VJsoA/exec"

        #JSON
        SetKey="Machine"
        SetValue="IoT Edge"
        InformationData = {}
        InformationData[SetKey]=SetValue
        InformationData["Machine ID"]=local_mac_address
        InformationData["Comm Type"]="Ethernet"
        InformationData["VibrationStatus"]=sVibrationStatus_Keep
        InformationData["FireDetectStatus"]=sFireDetectStatus
        InformationData["Gateway Time"]=datetime.now().strftime("%Y%m%d%H%M%S")	
        InformationData["Command"]="GetCommand"

        payload = {}
        headers= {}
        
        if bNetConnected or True:
            try:
                TransferJSONData=json.dumps(InformationData)

                try:
                    auth=('token', 'example')
                    ssl._create_default_https_context = ssl._create_unverified_context
                    headers = {'Content-Type': 'application/json'}
                    response = requests.request("POST", url, headers=headers, data=TransferJSONData)
                    data = response.json()

                    _command = data['Command']
                    print("\033[1;34mGet Command: " + _command + "\033[0m")
                except BaseException as error:
                    bNetConnected = False
                    print("\033[1;31mGet Command Failure\033[0m")

                if _command == "RecordVibration":
                    bRecordVibration = True

                if _command == "Reboot":
                    bRebootTrigger = True
                    bRunning = False

                if _command == "SetValue":
                    MyParameter.VibrationWarningValue=data['VibrationWarningValue']
                    MyParameter.VibrationAlarmValue=data['VibrationAlarmValue']
                    MyParameter.FireWarningTempValue=data['FireWarningTempValue']
                    MyParameter.FireWarningCountValue=data['FireWarningCountValue']
                    MyParameter.FireAlarmTempValue=data['FireAlarmTempValue']
                    MyParameter.FireAlarmCountValue=data['FireAlarmCountValue']
                    MyParameter.CapturePictureRH=data['CapturePictureRH']
                    MyParameter.CapturePictureRV=data['CapturePictureRV']
                    MyParameter.CaptureVideoSecond=data['CaptureVideoSecond']
                    MyParameter.SensorsFValue=data['SensorsFValue']
                    MyParameter.CameraFValue=data['CameraFValue']
                    MyParameter.UpdateFValue=data['UpdateFValue']
                    MyParameter.PhotoFolderID=data['PhotoFolderID']
                    MyParameter.VideoFolderID=data['VideoFolderID']

                    MyParameter.SaveParameter()

                    print("Set Value Completely")

                #CapturePicture
                #region
                if _command == "CapturePicture":
                    bManualCaptureImage = True
                
                #endregion

                if _command == "CaptureVideo":
                    bCaptureVideo = True

                if (bCaptureVideo and (bCameraUsed == False)):
                    print("    Start To Capture Video")
                    bCameraUsed = True
                    bCaptureVideo = False
                    #bconnected = os.system("ping -c 1 192.168.8.100")

                    nowtime = datetime.now()
                    datestring = nowtime.strftime('%Y%m%d')
                    fileString ="/home/pi/Pictures/CapVideo/" + datestring + "/"

                    if not os.path.isdir("/home/pi/Pictures/CapVideo/"):
                        os.mkdir("/home/pi/Pictures/CapVideo/")
                    if not os.path.isdir(fileString):
                        os.mkdir(fileString)
                    filename = "sn" + local_mac_address + nowtime.strftime('_%Y-%m-%d %H-%M-%S') + ".mp4"
                    fileString += filename

                    cap = cv2.VideoCapture(0)
                    encode = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(fileString, encode, 15.0, (640, 480))

                    start_time=time.time()
                    while(int(time.time()-start_time)<MyParameter.CaptureVideoSecond):
                        ret, frame = cap.read()
                        if ret == True:
                            showString3 = "Time:" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')# + "; Location: (260.252, 23.523)"
                            showString = "EnvTemp(" + str(temp_c) + "C), EnvHumidity(" + str(humidity) + "%RH)" 
                            showString2 = "Max Temp(" + str(thermalmaxValue) + "C), Min Temp(" + str(thermalminValue) + "C)"
                            cv2.putText(frame, showString3, (0, 420), cv2.FONT_HERSHEY_COMPLEX_SMALL , 1, (0, 255, 255), 1)
                            cv2.putText(frame, showString, (0, 440), cv2.FONT_HERSHEY_COMPLEX_SMALL , 1, (0, 255, 255), 1)
                            cv2.putText(frame, showString2, (0, 460), cv2.FONT_HERSHEY_COMPLEX_SMALL , 1, (0, 255, 255), 1)
                            out.write(frame)
                        else:
                            break
                    cap.release()
                    out.release()
                    cv2.destroyAllWindows()

                    time.sleep(5.0)

                    if True:
                        setsn=1
                        setfilename=filename
                        setdatetime=nowtime.strftime('%Y%m%d%H%M%S')

                        try:
                            if MyParameter.VideoFolderID != 'NA':
                                gauth = GoogleAuth()
                                gauth.CommandLineAuth() 
                                drive = GoogleDrive(gauth)

                                file1 = drive.CreateFile({'title': filename, 'mimeType':'image/jpeg','parents':[{'kind': 'drive#fileLink',
                                     'id': MyParameter.VideoFolderID }]}) 

                                file1.SetContentFile(fileString)
                                file1.Upload() 
                                print("\033[1;34mUpdate Capture Video Success\033[0m")
                            else:
                                print(ANSI_YELLOW + "    There is no update folder ID" + ANSI_OFF)
                        except:
                            print("\033[1;31mUpdate Capture Video Failure\033[0m")
                        file.close()
                    else:
                        print("\033[1;31mUpdate Capture Video Failure\033[0m")

                    bCameraUsed = False
            
            except:
                bNetConnected = False
                bCameraUsed = False
                print("\033[1;31mGet Command Failure\033[0m")

        print("\033[1;34mCheck Alarm Status-------------------------" + "\033[0m")
        #sVibrationStatus
        #region

        if ((sVibrationStatus_Keep != "Alarm") and bVibrationStatus):
            bVibrationStatus = False

        if(sVibrationStatus_Keep == "Alarm"):
            print(ANSI_RED + "Detect Vibration Alarm......................................................" + ANSI_OFF)
        elif(sVibrationStatus_Keep == "Warning"):
            print(ANSI_YELLOW + "Detect Vibration Warning......................................................" + ANSI_OFF)
        else:
            print(ANSI_GREEN + "Vibration Status is Normal................................................" + ANSI_OFF)
        
        if ((sVibrationStatus_Keep == "Alarm") and (bVibrationStatus==False)):
            bVibrationStatus = True
            bManualVibrationStatus = True

        #endregion

        #sFireDetectStatus
        #region
        if ((sFireDetectStatus != "Alarm") and bFireDetectStatus):
            bFireDetectStatus = False

        if(sFireDetectStatus == "Alarm"):
            print(ANSI_RED + "Detect Fire Alarm......................................................" + ANSI_OFF)
        elif(sFireDetectStatus == "Warning"):
            print(ANSI_RED + "Detect Fire Warning......................................................" + ANSI_OFF)
        else:
            print(ANSI_GREEN + "Not Detect Fire......................................................" + ANSI_OFF)
        
        bCaptureFromCamera = False
        if ((sFireDetectStatus == "Alarm") and (bFireDetectStatus==False) and (bCameraUsed == False)):
            print("    Start To Capture Image For Fire Detect Alarm")
            try:
                bCameraUsed = True
                bFireDetectStatus = True
                nowtime = datetime.now()
                datestring = nowtime.strftime('%Y%m%d')
                fileString ="/home/pi/Pictures/FireDetectPictures/" + datestring + "/"

                if not os.path.isdir("/home/pi/Pictures/FireDetectPictures/"):
                    os.mkdir("/home/pi/Pictures/FireDetectPictures/")
                if not os.path.isdir(fileString):
                    os.mkdir(fileString)
                filename = "sn_" + nowtime.strftime('%Y-%m-%d %H-%M-%S') + ".jpg"
                fileString += filename

                bCaptureFromCamera = True
                try:
                    with picamera.PiCamera() as camera:
                        camera.resolution = (MyParameter.CapturePictureRH,MyParameter.CapturePictureRV)
                        time.sleep(1.0)
                        camera.capture(fileString)
                        time.sleep(0.1)
                except:
                    bCaptureFromCamera = False
            except:
                print(ANSI_RED + "    Capture Image For Fire Alarm Error" + ANSI_OFF)

            if bCaptureFromCamera:
                setsn=1
                setfilename=filename
                setdatetime=nowtime.strftime('%Y%m%d%H%M%S')
                try:
                    if MyParameter.PhotoFolderID != 'NA':
                        gauth = GoogleAuth()
                        gauth.CommandLineAuth() 
                        drive = GoogleDrive(gauth)

                        file1 = drive.CreateFile({'title': filename, 'mimeType':'image/jpeg','parents':[{'kind': 'drive#fileLink',
                                     'id': MyParameter.PhotoFolderID }]}) 

                        file1.SetContentFile(fileString)
                        file1.Upload() 
                        print("\033[1;34mUpdate Capture Picture Success\033[0m")
                        FireAlarmData = {}
                        FireAlarmData["Machine ID"]=local_mac_address
                        FireAlarmData["Command"]="UpdateFireAlarmTrigger"
                        FireAlarmData["PhotoFileName"]=filename
                        FireAlarmData["VideoFileName"]="NA"
                        TransferJSONData=json.dumps(FireAlarmData)
                        try:
                            auth=('token', 'example')
                            ssl._create_default_https_context = ssl._create_unverified_context
                            headers = {'Content-Type': 'application/json'}
                            r = requests.post('https://script.google.com/macros/s/AKfycbyaqQfJagU3KR5ccgIfWkD99dLLtn-NQJbwNJ9siPdVU7VJsoA/exec',headers=headers, data=TransferJSONData, auth=auth)
                            print(ANSI_GREEN + "--Update Fire Alarm Trigger Success" + ANSI_OFF)
                        except BaseException as error:
                            print(ANSI_RED + "--Update Fire Alarm Trigger Failure" + ANSI_OFF)
                    else:
                        print(ANSI_YELLOW + "    There is no update folder ID" + ANSI_OFF)

                except:
                    print("\033[1;31mUpdate Capture Picture Failure\033[0m")
            else:
                print("\033[1;31mUpdate Capture Picture Failure\033[0m")

            TriggerAlarmToCloud()

            bCameraUsed = False
        #endregion

        time.sleep(5.0)

#endregion

#Update File To Google Drive
#region Update File To Google Drive

FireAlarmData={}
VibrationAlarmData = {}

def UpdateImageToGoogleDrive(filename, fileString, deletefile):
    try:
        if MyParameter.PhotoFolderID != 'NA':
            gauth = GoogleAuth()
            gauth.CommandLineAuth() 
            drive = GoogleDrive(gauth)

            file1 = drive.CreateFile({'title': filename, 'mimeType':'image/jpeg','parents':[{'kind': 'drive#fileLink',
                                     'id': MyParameter.PhotoFolderID }]}) 

            file1.SetContentFile(fileString)
            file1.Upload() 
            print("\033[1;34mUpdate Picture To Google Drive Success\033[0m")
            
            if deletefile == True:
                try: 
                    os.remove(fileString)
                    print(ANSI_GREEN + "    Delete Picture Success" + ANSI_OFF)
                except:
                    print(ANSI_RED + "    Delete Picture Failure" + ANSI_OFF)
        else:
            print(ANSI_YELLOW + "    There is no update folder ID" + ANSI_OFF)
    except:
        print("\033[1;31mUpdate Picture To Google Drive Failure\033[0m")

#endregion

#Update Local Picture
#region Update Local Picture

def VibrationAlarmTrigger():
    global FireAlarmData
    global VibrationAlarmData

    TransferJSONData=json.dumps(VibrationAlarmData)
    try:
        auth=('token', 'example')
        ssl._create_default_https_context = ssl._create_unverified_context
        headers = {'Content-Type': 'application/json'}
        r = requests.post('https://script.google.com/macros/s/AKfycbyaqQfJagU3KR5ccgIfWkD99dLLtn-NQJbwNJ9siPdVU7VJsoA/exec',headers=headers, data=TransferJSONData, auth=auth)
        print(ANSI_GREEN + "--Update Vibration Alarm Trigger Success" + ANSI_OFF)

        Thread.sleep(0.5)

        TriggerAlarmToCloud()

    except BaseException as error:
        print(ANSI_RED + "--Update Vibration Alarm Trigger Failure" + ANSI_OFF)

def UpdateLocalPicture():
    global bCameraUsed
    global local_mac_address

    #Manual Flag
    global bManualCaptureImage
    global bManualCaptureVideo
    global bManualVibrationStatus
    global bManualFireDetectStatus

    global FireAlarmData
    global VibrationAlarmData

    bManualCaptureImageKeep = False
    bManualCaptureVideoKeep = False
    bManualVibrationStatusKeep = False
    bManualFireDetectStatusKeep = False

    #print("Update Local Picture Start")
    tStart = time.time()

    time.sleep(3.0)

    bUpdate=True
    bUpdateKeep = False
    bUpdateRetry = False
    filename=''
    while bRunning:
        
        # Update Regular Image
        #region
        if (bUpdate and MyCamera.CheckCameraIdle()):
            bUpdate=False
            bUpdateKeep = True

            nowtime = datetime.now()
            datestring = nowtime.strftime('%Y%m%d')
            fileString ="/home/pi/Pictures/Pictures/" + datestring + "/"
            filename = MyCamera.CreateImageFileName(fileString, nowtime)
            fileString += filename

        if (bUpdateKeep and MyCamera.bCapturePictureError):
            bUpdateKeep = False
            if bUpdateRetry:
                bUpdateRetry = True
            else:
                bUpdateRetry = False
            MyCamera.bCapturePictureError = False

        if (bUpdateKeep and MyCamera.bCapturePictureDone):
            bUpdateKeep = False
            setfilename=filename
            setdatetime=nowtime.strftime('%Y%m%d%H%M%S')   

            UpdateImageToGoogleDrive(filename, fileString, True)
            MyCamera.bCapturePictureDone = False   

        #endregion

        # Manual Capture Image
        #region

        if (bManualCaptureImage and MyCamera.CheckCameraIdle()):
            bManualCaptureImage=False
            bManualCaptureImageKeep = True

            nowtime = datetime.now()
            datestring = nowtime.strftime('%Y%m%d')
            fileString ="/home/pi/Pictures/CapPictures/" + datestring + "/"
            filename = MyCamera.CreateImageFileName(fileString, nowtime, "/home/pi/Pictures/CapPictures/")
            fileString += filename

        if (bManualCaptureImageKeep and MyCamera.bCapturePictureError):
            bManualCaptureImageKeep = False

            MyCamera.bCapturePictureError = False


        if (bManualCaptureImageKeep and MyCamera.bCapturePictureDone):
            bManualCaptureImageKeep = False
            setfilename=filename
            setdatetime=nowtime.strftime('%Y%m%d%H%M%S')   

            UpdateImageToGoogleDrive(filename, fileString, False)
            MyCamera.bCapturePictureDone = False  

        #endregion

        # Vibaration Alarm Picture
        #region

        if (bManualVibrationStatus and MyCamera.CheckCameraIdle()):
            print("    Start To Capture Image For Vibration Alarm")
            bManualVibrationStatus=False
            bManualVibrationStatusKeep = True

            nowtime = datetime.now()
            datestring = nowtime.strftime('%Y%m%d')
            fileString ="/home/pi/Pictures/VibrationAlarmPictures/" + datestring + "/"
            filename = MyCamera.CreateImageFileName(fileString, nowtime, "/home/pi/Pictures/VibrationAlarmPictures/")
            fileString += filename

        if (bManualVibrationStatusKeep and MyCamera.bCapturePictureError):
            bManualVibrationStatusKeep = False

            MyCamera.bCapturePictureError = False

        if (bManualVibrationStatusKeep and MyCamera.bCapturePictureDone):
            bManualVibrationStatusKeep = False
            setfilename=filename
            setdatetime=nowtime.strftime('%Y%m%d%H%M%S')   
            VibrationAlarmData = {}
            VibrationAlarmData["Machine ID"]=local_mac_address
            VibrationAlarmData["Command"]="UpdateVibrationAlarmTrigger"
            VibrationAlarmData["PhotoFileName"]=filename
            VibrationAlarmData["VideoFileName"]="NA"
            UpdateImageToGoogleDrive(filename, fileString, True)
            VibrationAlarmTriggerThread = threading.Thread(target=VibrationAlarmTrigger)
            MyCamera.bCapturePictureDone = False  

        #endregion

        #Check Update Local Picture Timer      
        #region

        checktime = MyParameter.CameraFValue
        if bUpdateRetry:
            checktime = 30.0
        tEnd = time.time()
        intervalTime = tEnd - tStart
        if intervalTime >= MyParameter.CameraFValue:
            tStart=time.time()
            bUpdate=True

        #endregion

        time.sleep(0.1)
#endregion

#CameraFunction
#region

def CameraFunction():
    while bRunning:
        MyCamera.DoWork()

        time.sleep(0.1)

#endregion

print("\033[1;33mProgram Start\033[0m")

#Load Parameter
MyParameter.LoadParameter()

#Get Mac Address
hostname=socket.gethostname()
try:
    local_mac_address = get_mac_address()
except:
    local_mac_address='000000000000'
try:
    hostip = socket.gethostbyname(hostname)
except:
    hostip = '0.0.0.0'

print(ANSI_YELLOW + "Get Local Mac Address: " + local_mac_address + ANSI_OFF)


myBLEDevice = BLEDeviceForMi(True)
myBLEDevice.Start()

CameraThread = threading.Thread(target=CameraFunction)
GetLocalSensorsThread = threading.Thread(target=GetSensorsData)
UpdateSensorsThread = threading.Thread(target=UpdateLocalSensorsInformation)
UpdateLocalPictureThread = threading.Thread(target=UpdateLocalPicture)
GetCommandFromCloudThread = threading.Thread(target=GetCommandFromCloud)


CameraThread.start()
GetLocalSensorsThread.start()
UpdateSensorsThread.start()
UpdateLocalPictureThread.start()
GetCommandFromCloudThread.start()

try:
    #while bRunning:
        #time.sleep(1.0)
    print("Waiting for Finished!!")
    input()
except KeyboardInterrupt:
    bRunning=False

bRunning=False
myBLEDevice.Stop()

print("\033[1;33mProgram Finish\033[0m")

time.sleep(2.0)

if bRebootTrigger:
    print("\033[1;33mSystem Reboot\033[0m")
    time.sleep(5.0)
    os.system("sudo reboot")