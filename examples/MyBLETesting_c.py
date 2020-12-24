#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import os

import sys
import struct
import time
import threading
from bluepy.btle import UUID, Peripheral
from bluepy import btle

mac_address_list = []

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
            #print(data)
            if len(data) >= 3:
                data1 = data[0]
                data2 = data[1]
                data3 = data[2]
                data4 = float(data2 * 256 + data1) / 100.0
                print("Get Notification")
                print("Machine-" + str(self.index) + " => Get Temp:" + str(data4) + "C;   Humidity:" + str(data3) + "%RH")

class MyTest():
    BLE_Connected=False
    p=None
    bRunning=False
    DoWorkThread = 0
    start_time=time.time()
    ReconnectIntervalSecond = 10

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

                se10=self.p.getServiceByUUID('ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6')
                ch10=se10.getCharacteristics('ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6')
                ccc_desc = ch10[0].getDescriptors(forUUID=0x2902)[0]
                ccc_desc.write(b"\x02")
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
        while self.bRunning:
            if self.BLE_Connected:
                try:
                    self.p.waitForNotifications(0.5)
                except:
                    self.BLE_Connected = False
                    print("Machine-" + str(self.index) + " - Wait For Notification Error")
            else:
                if (int(time.time()-self.start_time)>self.ReconnectIntervalSecond):
                    self.start_time=time.time()
                    self.Connect()
            time.sleep(0.5)
    
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
    global mac_address_list
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
                        time.sleep(1.0)

                else:
                    print("There is no BLE Device")

                #endregion
            #endregion

            # Disconnect
            #region

            if self.bExecuteStop:
                self.bExecuteStop = False
                for index in range(length):
                    self.myBleDevice[index].Close()
                self.bRunning = False

            #endregion

            time.sleep(0.5)

def main():

    myBLEDevice = BLEDeviceForMi(True)
    myBLEDevice.Start()

    input()

    myBLEDevice.Stop()

 

if __name__ == "__main__":
    main()
