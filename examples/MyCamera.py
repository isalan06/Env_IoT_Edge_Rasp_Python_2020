#!/usr/bin/python3
#MyCamera.py

import os
import cv2
import picamera
import time
import datetime

import MyParameter

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

bCameraUsed = False
sImageFileName=''
bCapturePictureTrigger = False
bCapturePictureDone = False
bCapturePictureError = False
sSoftwareVersion='1.0.0.1'

def CheckCameraRunning():
    bResult = bCapturePictureTrigger or bCapturePictureDone or bCapturePictureError
    return bResult
def CheckCameraIdle():
    bResult = (bCapturePictureTrigger==False) and (bCapturePictureDone==False) and (bCapturePictureError==False)
    return bResult

def CreateImageFileName(folderString, nowtime, baseFolderString="/home/pi/Pictures/Pictures/"):
    global bCameraUsed
    global sImageFileName
    global bCapturePictureTrigger
    global bCapturePictureDone
    global bCapturePictureError

    bCapturePictureDone = False
    bCapturePictureError = False
    if not os.path.isdir(baseFolderString):
        os.mkdir(baseFolderString)
    if not os.path.isdir(folderString):
        os.mkdir(folderString)
    filename = "sn_" + nowtime.strftime('%Y-%m-%d %H-%M-%S') + ".jpg"
    sImageFileName = folderString + filename
    bCapturePictureTrigger = True
    return filename

def DoWork():
    global bCameraUsed
    global sImageFileName
    global bCapturePictureTrigger
    global bCapturePictureDone
    global bCapturePictureError
    if bCapturePictureTrigger == True:
        bCapturePictureTrigger = False

        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (MyParameter.CapturePictureRH,MyParameter.CapturePictureRV)
                time.sleep(0.1)
                camera.capture(sImageFileName)
                time.sleep(0.1)
                bCapturePictureDone = True
            print(ANSI_GREEN + "Capture Picture Success!" + ANSI_OFF)
        except:
            bCapturePictureError = True
            print(ANSI_RED + "Capture Picture Failure!" + ANSI_OFF)

    time.sleep(0.1)