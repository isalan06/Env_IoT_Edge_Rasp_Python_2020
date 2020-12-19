import sys
import struct
import time
import threading
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
    bRunning=False
    DoWorkThread = 0
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
                self.bRunning = True
                self.DoWorkThread = threading.Thread(target=self.DoWork)
                self.DoWorkThread.start()
        except:
            print("Connect Fail")
        finally:
            print("Finish")

    def DoWork(self):
        while self.bRunning:
            try:
                self.p.waitForNotifications(0.5)
            except:
                self.bRunning = False
                print("Machine-" + str(self.index) + " - Wait For Notification Error")
            time.sleep(0.5)
    
    def Close(self):
        self.bRunning = False
        if self.BLE_Connected == True:
            try:
                self.p.disconnect()
            except:
                self.p=None

def main():
    myTest2 = MyTest(2, 'a4:c1:38:0b:99:ed')
    myTest = MyTest(1, 'a4:c1:38:ee:b6:50')

    myTest.Connect()
    myTest2.Connect()

    myTest.Run()
    myTest2.Run()

    input()

    myTest.Close()
    myTest2.Close()

if __name__ == "__main__":
    main()
