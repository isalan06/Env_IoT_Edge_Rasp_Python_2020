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

sSoftwareVersion='1.0.0.3'
bCameraUsed = False
sImageFileName=''
bCapturePictureTrigger = False
bCapturePictureDone = False
bCapturePictureError = False

sVideoFileName = ''
bCaptureVideoTrigger = False
bCaptureVideoDone = False
bCaptureVideoError = False

def CheckCameraRunning():
    bResult = bCapturePictureTrigger or bCapturePictureDone or bCapturePictureError or bCaptureVideoTrigger or bCaptureVideoDone or bCaptureVideoError
    return bResult
def CheckCameraIdle():
    bResult = (bCapturePictureTrigger==False) and (bCapturePictureDone==False) and (bCapturePictureError==False) and (bCaptureVideoTrigger==False) and (bCaptureVideoDone==False) and (bCaptureVideoError==False)
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

def CreateVideoFileName(folderString, nowtime, baseFolderString="/home/pi/Pictures/CapVideo/"):
    global sVideoFileName
    global bCaptureVideoTrigger
    global bCaptureVideoDone
    global bCaptureVideoError

    bCaptureVideoDone = False
    bCaptureVideoError = False
    if not os.path.isdir(baseFolderString):
        os.mkdir(baseFolderString)
    if not os.path.isdir(fileString):
        os.mkdir(fileString)
    filename = "sn_" + nowtime.strftime('%Y-%m-%d %H-%M-%S')  + ".mp4"
    sVideoFileName = folderString +  filename
    bCaptureVideoTrigger = True
    return filename

def DoWork():
    global bCameraUsed
    global sImageFileName
    global bCapturePictureTrigger
    global bCapturePictureDone
    global bCapturePictureError
    global sVideoFileName
    global bCaptureVideoTrigger
    global bCaptureVideoDone
    global bCaptureVideoError
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

    if bCaptureVideoTrigger == True:
        bCaptureVideoTrigger = False
        try:
            cap = cv2.VideoCapture(0)
            encode = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(sVideoFileName, encode, 15.0, (640, 480))

            start_time=time.time()
            while(int(time.time()-start_time)<MyParameter.CaptureVideoSecond):
                ret, frame = cap.read()
                if ret == True:
                    #showString3 = "Time:" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')# + "; Location: (260.252, 23.523)"
                    #showString = "EnvTemp(" + str(temp_c) + "C), EnvHumidity(" + str(humidity) + "%RH)" 
                    #showString2 = "Max Temp(" + str(thermalmaxValue) + "C), Min Temp(" + str(thermalminValue) + "C)"
                    #cv2.putText(frame, showString3, (0, 420), cv2.FONT_HERSHEY_COMPLEX_SMALL , 1, (0, 255, 255), 1)
                    #cv2.putText(frame, showString, (0, 440), cv2.FONT_HERSHEY_COMPLEX_SMALL , 1, (0, 255, 255), 1)
                    #cv2.putText(frame, showString2, (0, 460), cv2.FONT_HERSHEY_COMPLEX_SMALL , 1, (0, 255, 255), 1)
                    out.write(frame)
                else:
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()
            bCaptureVideoDone = True
            print(ANSI_GREEN + "Capture Video Success!" + ANSI_OFF)
        except:
            bCaptureVideoError = True
            print(ANSI_RED + "Capture Video Failure!" + ANSI_OFF)

    time.sleep(0.1)