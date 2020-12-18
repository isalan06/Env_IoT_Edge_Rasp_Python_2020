import sys
import struct
from bluepy.btle import UUID, Peripheral
from bluepy import btle

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

print("Start To Connect BLE")
p = Peripheral('a4:c1:38:ee:b6:50')
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
        print("Set Notification")
        print(ch10[0].valHandle+1)
        p.writeCharacteristic(ch10[0].valHandle+1, "\x02\x00")
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