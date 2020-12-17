#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import os
import sys
import struct
from bluepy.btle import UUID, Peripheral
from bluepy import btle

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

#dump_services
#region dump_services

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

#endregion

#class Scan Print
#region

class ScanPrint(btle.DefaultDelegate):

    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleDiscovery(self, dev, isNewDev, isNewData):
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

        #print ('    Device (%s): %s (%s), %d dBm %s' %
        #       (status,
        #           ANSI_WHITE + dev.addr + ANSI_OFF,
        #           dev.addrType,
        #           dev.rssi,
        #           ('' if dev.connectable else '(not connectable)'))
        #       )
        for (sdid, desc, val) in dev.getScanData():
            #if sdid in [8, 9]:
            #    print ('\t' + desc + ': \'' + ANSI_CYAN + val + ANSI_OFF + '\'')
            #else:
            #    print ('\t' + desc + ': <' + val + '>')

            if(desc == 'Complete Local Name'):
                if(val == 'LYWSD03MMC'):
                    print ('\t' + ANSI_RED + 'Get Sensors Address: %s' % (dev.addr) + ANSI_OFF)

        if not dev.scanData:
            print ('\t(no data)')
        print

#endregion

#class MyDelegate
#region
class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        print("Delegate initial Success")

    def handleNotification(self, cHandle, data):
            #print(data)
            if len(data) >= 3:
                data1 = data[0]
                data2 = data[1]
                data3 = data[2]
                data4 = float(data2 * 256 + data1) / 100.0
                print("Get Temp:" + str(data4) + "C;   Humidity:" + str(data3) + "%RH")

#endregion

#class MyBLEReceiver
#region
class MyBLEReceiver():
    def __init__(self, index, mac_address):
        self.index=index
        self.mac_address=mac_address

#endregion

if __name__ == "__main__":
    main()

def main():
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
    devices = scanner.scan(10)

    if arg.discover:
        print (ANSI_RED + "Discovering services..." + ANSI_OFF)

        for d in devices:
            if not d.connectable or d.rssi < arg.sensitivity:

                continue

            print ("    Connecting to", ANSI_WHITE + d.addr + ANSI_OFF + ":")

            dev = btle.Peripheral(d)
            dump_services(dev)
            dev.disconnect()
            print

print("Start To Connect BLE")
p = Peripheral('a4:c1:38:0b:99:ed')
p.setDelegate(MyDelegate())
try:
    chList=p.getCharacteristics()


    seList=p.getServices()
    for se in seList:
        try:
            print(se.uuid)
        except:
            print("SE Error")

    print("---------------------------")
    print("Get Service1")


    try:
        se1=p.getServiceByUUID('0000180f-0000-1000-8000-00805f9b34fb')
        ch1=se1.getCharacteristics('00002a19-0000-1000-8000-00805f9b34fb')

        for _ch1 in ch1:
            print(_ch1.uuid)

        print("----------------------------------")
        print(ch1[0].uuid)
        print(ch1[0].read())
    except:
        print("SE1 Error")

    print("-------------------------------------------")
    print("Get Data")
    try:
        se10=p.getServiceByUUID('ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6')
        print("------------------------")
        print(se10)
        ch10=se10.getCharacteristics('ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6')
        print("-------------------------")
        print(ch10)
        print("---------------------------------")
        #print("Set Notification")
        #print(ch.getHandle())
        #p.setDelegate(MyDelegate())
        #print("Set Notification Success")

        #print(ch10[0].uuid)
        #print(ch10[0].read())
    except:
        print("Get Data Error")


    for i in range(1, 100):
        if p.waitForNotifications(1.0):
            print("----------------------")
        #print("Waiting..."+str(i))

except:
    print("Connect Fail")
finally:
    print("Finish")
    p.disconnect()
