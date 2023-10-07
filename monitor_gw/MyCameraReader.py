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

class CameraDataDto:
    def __init__(self) -> None:
        pass

CameraData = CameraDataDto()

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
        while (self.bFinished == False):

            if(self.bStart) and (self.camera != None):
                try:
                    self.camera.capture(self.rawCapture, format="bgr")
                    image = self.rawCapture.array
                    MyPrint.Print_Yellow('Camera read image success', CameraInfoString)
                except Exception as e:
                    MyPrint.Print_Red('Camera read image failure', CameraErrorString)
                    print(e)

            time.sleep(5.0)

        if self.camera != None:
            self.camera.close()
            self.camera = None

        MyPrint.Print_Cyan('Camera module is finished', CameraInfoString)

