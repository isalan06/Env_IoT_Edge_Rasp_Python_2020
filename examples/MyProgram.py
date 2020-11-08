#!/usr/bin/python3

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

import os
import picamera

#Flag
bRunning = True
bGetData = False
bNetConnected = True

#Alarm Status
sVibrationStatus = "Normal"
sFireDetectStatus = "Normal"

#Parameter
VibrationWarningValue=30.0
VibrationAlarmValue=50.0
FireWarningTempValue=50.0
FireWarningCountValue=4
FireAlarmTempValue=70.0
FireAlarmCountVaue=1
CapturePictureRH=1920
CapturePictureRV=1080
CaptureVideoSecond=15

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

    #Parameter
    global VibrationWarningValue
    global VibrationAlarmValue
    global FireWarningTempValue
    global FireWarningCountValue
    global FireAlarmTempValue
    global FireAlarmCountVaue

    #AMG8833 Attribute
    global thermalpixels

    print("Get Local Sensors Thread Start")

    # DHT22 Attribute
    dhtDevice = adafruit_dht.DHT22(board.D17)

   
    

    #AMG8833 Attribute
    thermalImage = Adafruit_AMG88xx()

    while bRunning:

        #DHT22
        try:
            temp_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print("Temp: {:.1f}C Humidity: {}%".format(temp_c, humidity))
        except RuntimeError as error:
            print("Get DHT Error: " + error.args[0])

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
            #print("gyro_xout:" + str(gyro_xout) + "-" + str(gyro_xout_scaled) + ";gyro_yout:" + str(gyro_yout) + "-" + str(gyro_yout_scaled) + ";gyro_zout:" + str(gyro_zout) + "-" + str(gyro_zout_scaled))
            #print("accel_xout:" + str(accel_xout) + "-" + str(accel_xout_scaled) + ";accel_yout:" + str(accel_yout) + "-" + str(accel_yout_scaled) + ";accel_zout:" + str(accel_zout) + "-" + str(accel_zout_scaled))
            #print("x_rotation:" + str(x_rotation) + ";y_rotation:" + str(y_rotation))
            if (gyro_xout_scaled > VibrationAlarmValue) or (gyro_yout_scaled > VibrationAlarmValue) or (gyro_zout_scaled > VibrationAlarmValue):
                sVibrationStatus = "Alarm"
            elif (gyro_xout_scaled > VibrationWarningValue) or (gyro_yout_scaled > VibrationWarningValue) or (gyro_zout_scaled > VibrationWarningValue):
                sVibrationStatus = "Warning"
            else:
                sVibrationStatus = "Normal"
            print("Get G Sensors Success: " + sVibrationStatus)
        except:
            print("Get G Sensor Failure")
            

        #Thermal Image
        try:
            thermalpixels = thermalImage.readPixels()

            fireAlarmCount=0
            fireWarningCount=0
            for i in thermalpixels:
                if i >FireAlarmTempValue:
                    fireAlarmCount += 1
                elif i > FireWarningTempValue:
                    fireWarningCount += 1

            if fireAlarmCount > FireAlarmCountVaue:
                sFireDetectStatus="Alarm"
            elif fireWarningCount > FireWarningCountValue:
                sFireDetectStatus="Warning"
            else:
                sFireDetectStatus="Normal"


            print("Get ThermalPixels Success: " + sFireDetectStatus)
        except:
            print("Get TermalPixels Failure")
            

        bGetData = True

        time.sleep(3.0)

def UpdateLocalSensorsInformation():

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

    #AMG8833 Attribute
    global thermalpixels

    print("Update Sensors Informatnio Start")
    while bRunning:
        time.sleep(5.0)
        if bGetData & bNetConnected:
            bGetData = False

            #JSON
            SetKey="Machine"
            SetValue="IoT Edge"
            InformationData = {}
            InformationData[SetKey]=SetValue
            InformationData["Machine ID"]="Test ID"
            InformationData["Comm Type"]="Ethernet"
            InformationData["VibrationStatus"]=sVibrationStatus
            InformationData["FireDetectStatus"]=sFireDetectStatus
            InformationData["Gateway Time"]=datetime.now().strftime("%Y%m%d%H%M%S")	
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

            try:
                auth=('token', 'example')
                ssl._create_default_https_context = ssl._create_unverified_context
                headers = {'Content-Type': 'application/json'}
                r = requests.post('https://script.google.com/macros/s/AKfycbwOx-ypSoziN9f9__rit-_J3bjYP8sSOPoIfzo1rqi3QRIl-DQ/exec',headers=headers, data=TransferJSONData, auth=auth)
                print("Update Sensors Information Success")
            except BaseException as error:
                print("Update Sensors Information Failure")

def GetCommandFromCloud():
    global bRunning
    global bNetConnected

    #Parameter
    global VibrationWarningValue
    global VibrationAlarmValue
    global FireWarningTempValue
    global FireWarningCountValue
    global FireAlarmTempValue
    global FireAlarmCountVaue
    global CapturePictureRH
    global CapturePictureRV
    global CaptureVideoSecond

    print("Get Command From Cloud")
    
    while bRunning:

        url = "https://script.google.com/macros/s/AKfycbwOx-ypSoziN9f9__rit-_J3bjYP8sSOPoIfzo1rqi3QRIl-DQ/exec"

        payload = {}
        headers= {}

        response = requests.request("GET", url, headers=headers, data = payload)
        #response.text.encode('utf8')
        data = response.json()

        _command = data['Command']
        print("Get Command: " + _command)
        if _command == "SetValue":
            VibrationWarningValue=data['VibrationWarningValue']
            VibrationAlarmValue=data['VibrationAlarmValue']
            FireWarningTempValue=data['FireWarningTempValue']
            FireWarningCountValue=data['FireWarningCountValue']
            FireAlarmTempValue=data['FireAlarmTempValue']
            FireAlarmCountVaue=data['FileAlarmCountValue']
            CapturePictureRH=data['CapturePictureRH']
            CapturePictureRV=data['CapturePictureRV']
            CaptureVideoSecond=data['CaptureVideoSecond']
            print("Set Value Completely")
        if _command == "CapturePicture":
            bconnected = os.system("ping -c 1 192.168.8.100")

            nowtime = datetime.now()
            datestring = nowtime.strftime('%Y%m%d')
            fileString ="CapPictures/" + datestring + "/"

            if not os.path.isdir("CapPictures/"):
                os.mkdir("CapPictures/")
            if not os.path.isdir(fileString):
                os.mkdir(fileString)
            filename = nowtime.strftime('%Y%m%d%H%M%S') + ".jpg"
            fileString += filename

            with picamera.PiCamera() as camera:
                camera.resolution = (CapturePictureRH,CapturePictureRV)
                time.sleep(1.0)
                camera.capture(fileString)

            if bconnected == 0:
                setsn=1
                setfilename=filename
                setdatetime=nowtime.strftime('%Y%m%d%H%M%S')
                url = "http://192.168.8.100:5099/Update/JpgCapPicture?sn=" + str(setsn) + "&filename=" + setfilename + "&datetime=" + setdatetime
                file=open(fileString ,'rb')
                payload=file.read()
                file.close()
                headers = {'Content-Type': 'image/jpeg'}
                responses = requests.request("POST", url, headers=headers, data = payload)
                print(responses.text.encode('utf8'))

        if _command == "CaptureVideo":
            bconnected = os.system("ping -c 1 192.168.8.100")

            nowtime = datetime.now()
            datestring = nowtime.strftime('%Y%m%d')
            fileString ="CapVideo/" + datestring + "/"

            if not os.path.isdir("CapVideo/"):
                os.mkdir("CapVideo/")
            if not os.path.isdir(fileString):
                os.mkdir(fileString)
            filename = nowtime.strftime('%Y%m%d%H%M%S') + ".mp4"
            fileString += filename

            cap = cv2.VideoCapture(0)            encode = cv2.VideoWriter_fourcc(*'mp4v')            out = cv2.VideoWriter(fileString, encode, 20.0, (640, 480))            start_time=time.time()            while(int(time.time()-start_time)<CaptureVideoSecond):                ret, frame = cap.read()                if ret == True:                    out.write(frame)                else:                    break            cap.release()            out.release()            cv2.destroyAllWindows()
            if bconnected == 0:
                setsn=1
                setfilename=filename
                setdatetime=nowtime.strftime('%Y%m%d%H%M%S')
                url = "http://192.168.8.100:5099/Update/CapVideo?sn=" + str(setsn) + "&filename=" + setfilename + "&datetime=" + setdatetime
                file=open(fileString ,'rb')
                payload=file.read()
                file.close()
                headers = {'Content-Type': 'video/mp4'}
                responses = requests.request("POST", url, headers=headers, data = payload)
                print(responses.text.encode('utf8'))

        time.sleep(1.0)



def UpdateLocalPicture():
    print("Update Local Picture Start")
    while bRunning:
        bconnected = os.system("ping -c 1 192.168.8.100")

        nowtime = datetime.now()
        datestring = nowtime.strftime('%Y%m%d')
        fileString ="Pictures/" + datestring + "/"

        if not os.path.isdir("Pictures/"):
            os.mkdir("Pictures/")
        if not os.path.isdir(fileString):
            os.mkdir(fileString)
        filename = nowtime.strftime('%Y%m%d%H%M%S') + ".jpg"
        fileString += filename

        with picamera.PiCamera() as camera:
            camera.resolution = (1024,768)
            time.sleep(1.0)
            camera.capture(fileString)

        if bconnected == 0:
            setsn=1
            setfilename=filename
            setdatetime=nowtime.strftime('%Y%m%d%H%M%S')
            url = "http://192.168.8.100:5099/Update/JpgPicture?sn=" + str(setsn) + "&filename=" + setfilename + "&datetime=" + setdatetime
            file=open(fileString ,'rb')
            payload=file.read()
            file.close()
            headers = {'Content-Type': 'image/jpeg'}
            responses = requests.request("POST", url, headers=headers, data = payload)
            print(responses.text.encode('utf8'))

        time.sleep(300.0)

GetLocalSensorsThread = threading.Thread(target=GetSensorsData)
UpdateSensorsThread = threading.Thread(target=UpdateLocalSensorsInformation)
UpdateLocalPictureThread = threading.Thread(target=UpdateLocalPicture)
GetCommandFromCloudThread = threading.Thread(target=GetCommandFromCloud)
GetLocalSensorsThread.start()
UpdateSensorsThread.start()
UpdateLocalPictureThread.start()
GetCommandFromCloudThread.start()

GetLocalSensorsThread.join()
UpdateSensorsThread.join()
UpdateLocalPictureThread.join()
GetCommandFromCloudThread.join()

try:
    while True:
        time.sleep(10.0)
except KeyboardInterrupt:
    bRunning=False
    print("Program Finish")

bRunning=False