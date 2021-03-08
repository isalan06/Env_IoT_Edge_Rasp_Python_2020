#!/usr/bin/python3
#MyCamera.py

import os
import cv2
import picamera
import time
import datetime

import MyParameter

bCameraUsed = False
sImageFileName=''
bCapturePictureTrigger = False
bCapturePictureDone = False
bCapturePictureError = False

def CheckCameraRunning():
    bResult = bCapturePictureTrigger or bCapturePictureDone or bCapturePictureError
    return bResult
def CheckCameraIdle():
    bResult = (bCapturePictureTrigger==False) and (bCapturePictureDone==False) and (bCapturePictureError==False)
    return bResult

def CreateImageFileName(folderString, nowtime):
    bCapturePictureDone = False
    bCapturePictureError = False
    if not os.path.isdir("/home/pi/Pictures/Pictures/"):
        os.mkdir("/home/pi/Pictures/Pictures/")
    if not os.path.isdir(folderString):
        os.mkdir(folderString)
    filename = "sn_" + nowtime.strftime('%Y-%m-%d %H-%M-%S') + ".jpg"
    sImageFileName = folderString + filename
    bCapturePictureTrigger = True
    return filename

def DoWork():
    if bCapturePictureTrigger == True:
        bCapturePictureTrigger = False

        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (1024,768)
                time.sleep(0.1)
                camera.capture(fileString)
                time.sleep(0.1)
                bCapturePictureDone = True
        except:
            bCapturePictureError = True

    time.sleep(0.1)