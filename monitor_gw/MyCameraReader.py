#!/usr/bin/python3
#MyCameraReader.py

import MyPrint

import os
import cv2
import picamera
import time
import datetime

from picamera.array import PiRGBArray
from picamera import PiCamera

import base64
from PIL import Image
from io import BytesIO

import threading

from imutils.video import VideoStream

CameraInfoString = '[Camera Info]'
CameraErrorString = '[Camera Info]'
CameraFunInfoString = '[Camera Function Info]'
CameraFunErrorString = '[Camera Function Info]'

class CameraDataDto:

    ReCaptureCameraImageTime = 0.5
    NormalCaptureCameraTimeValue = 0.5
    ErrorCaptureCameraTimeValue = 5.0
    bImageHandleError = False

    NormalImageByteArray=0
    bNormalImageTransferSuccess=False

    ImageGrayMean=0.0
    sSmallImageData=''
    sSmallImageData2=''
    iSmallImageIndex=-1
    sSmallImageTime='NA'
    bSmallImageTrigger = 0

    sNormalImageData=''
    sNormalImageData2=''
    iNormalImageIndex=-1
    sNormalImageTime='NA'
    bNormalImageTrigger = 0

    ImageGrayMean = 0.0

    def __init__(self) -> None:
        pass

CameraData = CameraDataDto()

def frame2ByteArray(frame):
    global CameraData

    try:
        img = Image.fromarray(frame) #將每一幀轉為Image
        output_buffer = BytesIO() #建立一個BytesIO
        img.save(output_buffer, format='JPEG') #寫入output_buffer
        NormalImageByteArray = output_buffer.getvalue() #在記憶體中讀取
        CameraData.bNormalImageTransferSuccess = True

        try:   
            if CameraData.iNormalImageIndex != 0:
                CameraData.sNormalImageData = (base64.b64encode(NormalImageByteArray)).decode('utf-8') #轉為BASE64
                CameraData.iNormalImageIndex = 0
            else:
                CameraData.sNormalImageData2 = (base64.b64encode(NormalImageByteArray)).decode('utf-8') #轉為BASE64
                CameraData.iNormalImageIndex = 1

            CameraData.sNormalImageTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        except:
            MyPrint.Print_Red('Transfer Base64 Failure', CameraFunErrorString)
            CameraData.bImageHandleError = True


        #MyPrint.Print_Green('Transfer Normal Image Data Success', CameraFunInfoString)
    except:
        CameraData.bNormalImageTransferSuccess = False
        MyPrint.Print_Red('Transfer Normal Image Data Failure', CameraFunErrorString)
        CameraData.bImageHandleError = True

def frame2base64(frame):
    global CameraData

    try:
        img = Image.fromarray(frame) #將每一幀轉為Image
        output_buffer = BytesIO() #建立一個BytesIO
        img.save(output_buffer, format='JPEG') #寫入output_buffer
        byte_data = output_buffer.getvalue() #在記憶體中讀取

        try:   
            if CameraData.iSmallImageIndex != 0:
                CameraData.sSmallImageData = (base64.b64encode(byte_data)).decode('utf-8') #轉為BASE64
                CameraData.iSmallImageIndex = 0
            else:
                CameraData.sSmallImageData2 = (base64.b64encode(byte_data)).decode('utf-8') #轉為BASE64
                CameraData.iSmallImageIndex = 1

            CameraData.sSmallImageTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        except:
            MyPrint.Print_Red('Transfer Base64 Failure', CameraFunErrorString)
            CameraData.bImageHandleError = True

        #MyPrint.Print_Green('Transfer Small Image Data Success', CameraFunInfoString)
    except:
        MyPrint.Print_Green('Transfer Small Image Data Failure', CameraFunErrorString)
        CameraData.bImageHandleError = True

class CameraReader:
    camera = None
    bFinished = False
    bStart = False
    rawCapture = None
    CameraThread = None
    
    def __init__(self) -> None:
        pass

    def Start(self):
        if (self.camera == None) and (self.bStart == False):
            try:
                self.camera = PiCamera()
                #self.camera.shutter_speed=MyParameter.C_ShutterSpeed
                #self.camera.rotation=MyParameter.C_Rotation
                self.camera.resolution = (1920, 1088)
                self.rawCapture = PiRGBArray(self.camera, size=(1920, 1088))
                self.bStart = True
                self.CameraThread = threading.Thread(target=self.DoWork)
                self.CameraThread.start()
                MyPrint.Print_Green("Camera initialize Success", CameraInfoString)
            except:
                MyPrint.Print_Red("Camera initialize Failure", CameraErrorString)

    def Stop(self):
        self.bFinished = True

    def DoWork(self):
        global CameraData

        while (self.bFinished == False):
            CameraData.bImageHandleError = False
            if(self.bStart) and (self.camera != None):
                try:
                    rawCapture = PiRGBArray(self.camera, size=(1920, 1088))


                    self.camera.capture(rawCapture, format="bgr")
                    image = rawCapture.array

                    # Transfer Normal Image to Base64
                    frame2ByteArray(image)

                    # Transfer Normal Image to Gray Image
                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    CameraData.ImageGrayMean = gray_image.mean()

                    # Create Small Image and transfer it to Base64
                    new_image = cv2.resize(image, (480, 320), interpolation=cv2.INTER_AREA)
                    frame2base64(new_image)
                    CameraData.bSmallImageTrigger = 1

                    #MyPrint.Print_Yellow('Camera read image success', CameraInfoString)
                except Exception as e:
                    CameraData.bImageHandleError = True
                    MyPrint.Print_Red('Camera read image failure', CameraErrorString)
                    print(e)


            if CameraData.bImageHandleError:
                CameraData.ReCaptureCameraImageTime = CameraData.ErrorCaptureCameraTimeValue
            else:
                CameraData.ReCaptureCameraImageTime = CameraData.NormalCaptureCameraTimeValue
            time.sleep(CameraData.ReCaptureCameraImageTime)

        if self.camera != None:
            self.camera.close()
            self.camera = None

        MyPrint.Print_Cyan('Camera module is finished', CameraInfoString)

