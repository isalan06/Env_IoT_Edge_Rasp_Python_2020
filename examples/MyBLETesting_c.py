import sys
import struct
from bluepy.btle import UUID, Peripheral
from bluepy import btle

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
    def __init__(self, index, mac_address):
        self.index=index
        self.mac_address=mac_address

    def Connect(self):
        print("Start To Connect BLE-" + str(self.index))
        try:
            self.p = Peripheral(self.mac_address)
            self.p.setDelegate(MyDelegate(self.index))
            self.BLE_Connected = True
        except:
            self.BLE_Connected = False

    def Run(self):
        try:
            if self.BLE_Connected == True:
                for i in range(1, 20):
                    if p.waitForNotifications(1.0):
                        print("----------------------")
        except:
            print("Connect Fail")
        finally:
            print("Finish")
    
    def Close(self):
        if self.BLE_Connected == True:
            try:
                self.p.disconnect()
            except:
                self.p=None

def main():
    myTest = MyTest(1, 'a4:c1:38:0b:99:ed')
    myTest2 = MyTest(2, 'a4:c1:38:ee:b6:50')

    myTest.Connect()
    myTest2.Connect()

    myTest.Run()
    myTest2.Run()

    myTest.Close()
    myTest2.Close()

if __name__ == "__main__":
    main()
