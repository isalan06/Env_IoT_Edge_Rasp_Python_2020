#!/usr/bin/python3
#MyCamera.py

import os
import cv2
import picamera
import time
import datetime

from picamera.array import PiRGBArray
from picamera import PiCamera

import MyParameter

import base64
from PIL import Image
from io import BytesIO

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

sSoftwareVersion='1.0.3.0'
bCameraUsed = False
sImageFileName=''
bCapturePictureTrigger = False
bCapturePictureDone = False
bCapturePictureError = False

sVideoFileName = ''
bCaptureVideoTrigger = False
bCaptureVideoDone = False
bCaptureVideoError = False

tCheckImageTimer_Start = time.time()

iCameraCount = 0

#Camera Function Data
ImageGrayMean=0.0
sSmallImageData=''
sSmallImageData2=''
iSmallImageIndex=-1
sSmallImageTime='NA'
bSmallImageTrigger = 0

def frame2base64(frame):
    global sSmallImageData
    global sSmallImageData2
    global iSmallImageIndex
    global sSmallImageTime

    try:
        img = Image.fromarray(frame) #將每一幀轉為Image
        output_buffer = BytesIO() #建立一個BytesIO
        img.save(output_buffer, format='JPEG') #寫入output_buffer
        byte_data = output_buffer.getvalue() #在記憶體中讀取

        try:   
            if iSmallImageIndex != 0:
                sSmallImageData = (base64.b64encode(byte_data)).decode('utf-8') #轉為BASE64
                iSmallImageIndex = 0
            else:
                sSmallImageData2 = (base64.b64encode(byte_data)).decode('utf-8') #轉為BASE64
                iSmallImageIndex = 1

            sSmallImageTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        except:
            print(ANSI_RED + 'Transfer Base64 Failure' + ANSI_OFF)

        print('Transfer Image Data Success')
    except:
        print(ANSI_RED + 'Transfer Image Data Failure' + ANSI_OFF)

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
    if not os.path.isdir(folderString):
        os.mkdir(folderString)
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

    global tCheckImageTimer_Start
    global ImageGrayMean
    global sSmallImageData
    
    global iCameraCount
    global bSmallImageTrigger

    checkCameraFunctionIntervalTime = time.time() - tCheckImageTimer_Start
    #print(checkCameraFunctionIntervalTime)
    if checkCameraFunctionIntervalTime >= 2:
        
        if MyParameter.CameraFunctionFlag != 0:
            #print("Start To Check Camera Function")

            try:
            # initialize the camera and grab a reference to the raw camera capture
                with picamera.PiCamera() as camera:
                    #camera.shutter_speed=100
                    #camera.resolution = (480, 320)
                    #rawCapture = PiRGBArray(camera, size=(480, 320))
                    camera.shutter_speed=MyParameter.C_ShutterSpeed
                    camera.rotation=MyParameter.C_Rotation
                    camera.resolution = (1920, 1088)
                    rawCapture = PiRGBArray(camera, size=(1920, 1088))
                    # allow the camera to warmup
                    time.sleep(0.1)
                    # grab an image from the camera
                    camera.capture(rawCapture, format="bgr")
                    image = rawCapture.array

                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    ImageGrayMean = gray_image.mean()
                    new_image = cv2.resize(image, (480, 320), interpolation=cv2.INTER_AREA)
                    print(ImageGrayMean)
                    frame2base64(new_image)
                    bSmallImageTrigger = 1
            except:
                print(ANSI_RED + 'Transfer Image Error' + ANSI_OFF)

        time.sleep(0.5)
        tCheckImageTimer_Start = time.time()




    if bCapturePictureTrigger == True:
        bCapturePictureTrigger = False

        try:
            with picamera.PiCamera() as camera:
                camera.shutter_speed=MyParameter.C_ShutterSpeed
                camera.rotation=MyParameter.C_Rotation
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

    iCameraCount = iCameraCount + 1
    if iCameraCount >= 1000:
        iCameraCount = 0    

    time.sleep(0.5)