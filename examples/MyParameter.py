#!/usr/bin/python3
#MyParameter.py
import os
import configparser
import RPi.GPIO as GPIO

sSoftwareVersion='1.0.0.1'

#Parameter
VibrationWarningValue=30.0
VibrationAlarmValue=50.0
FireWarningTempValue=50.0
FireWarningCountValue=4
FireAlarmTempValue=70.0
FireAlarmCountValue=1
CapturePictureRH=1920
CapturePictureRV=1080
CaptureVideoSecond=15
SensorsFValue=3.0
CameraFValue=300.0
UpdateFValue=10.0
PhotoFolderID="NA"
VideoFolderID="NA"

rled=24
gled=23


#Parameter function           
#region Parameter function

def CreateParameter():
    #Parameter
    global VibrationWarningValue
    global VibrationAlarmValue
    global FireWarningTempValue
    global FireWarningCountValue
    global FireAlarmTempValue
    global FireAlarmCountValue
    global CapturePictureRH
    global CapturePictureRV
    global CaptureVideoSecond
    global SensorsFValue
    global CameraFValue
    global UpdateFValue
    global PhotoFolderID
    global VideoFolderID

    if not os.path.isdir("/home/pi/Parameter/"):
        os.mkdir("/home/pi/Parameter/")
    filePathString = "/home/pi/Parameter/Parameter.ini"

    config = configparser.ConfigParser()
    config['Parameter'] = {} 
    config['Parameter']['VibrationWarningValue'] = str(VibrationWarningValue)
    config['Parameter']['VibrationAlarmValue'] = str(VibrationAlarmValue)
    config['Parameter']['FireWarningTempValue'] = str(FireWarningTempValue)
    config['Parameter']['FireWarningCountValue'] = str(FireWarningCountValue)
    config['Parameter']['FireAlarmTempValue'] = str(FireAlarmTempValue)
    config['Parameter']['FireAlarmCountValue'] = str(FireAlarmCountValue)
    config['Parameter']['CapturePictureRH'] = str(CapturePictureRH)
    config['Parameter']['CapturePictureRV'] = str(CapturePictureRV)
    config['Parameter']['CaptureVideoSecond'] = str(CaptureVideoSecond)
    config['Parameter']['SensorsFValue'] = str(SensorsFValue)
    config['Parameter']['CameraFValue'] = str(CameraFValue)
    config['Parameter']['UpdateFValue'] = str(UpdateFValue)
    config['Parameter']['PhotoFolderID'] = PhotoFolderID
    config['Parameter']['VideoFolderID'] = VideoFolderID

    with open(filePathString, 'w') as configfile:
        config.write(configfile)


def LoadParameter():
    #Parameter
    global VibrationWarningValue
    global VibrationAlarmValue
    global FireWarningTempValue
    global FireWarningCountValue
    global FireAlarmTempValue
    global FireAlarmCountValue
    global CapturePictureRH
    global CapturePictureRV
    global CaptureVideoSecond
    global SensorsFValue
    global CameraFValue
    global UpdateFValue
    global PhotoFolderID
    global VideoFolderID

    filePathString = "/home/pi/Parameter/Parameter.ini"

    if os.path.isfile(filePathString):
        config = configparser.ConfigParser()
        config.read(filePathString)
        VibrationWarningValue = config['Parameter'].getfloat('VibrationWarningValue')
        VibrationAlarmValue = config['Parameter'].getfloat('VibrationAlarmValue')
        FireWarningTempValue = config['Parameter'].getfloat('FireWarningTempValue')
        FireWarningCountValue = config['Parameter'].getint('FireWarningCountValue')
        FireAlarmTempValue = config['Parameter'].getfloat('FireAlarmTempValue')
        FireAlarmCountValue = config['Parameter'].getint('FireAlarmCountValue')
        CapturePictureRH = config['Parameter'].getint('CapturePictureRH')
        CapturePictureRV = config['Parameter'].getint('CapturePictureRV')
        CaptureVideoSecond = config['Parameter'].getint('CaptureVideoSecond')
        SensorsFValue = config['Parameter'].getfloat('SensorsFValue')
        CameraFValue = config['Parameter'].getfloat('CameraFValue')
        UpdateFValue = config['Parameter'].getfloat('UpdateFValue')
        PhotoFolderID = config['Parameter']['PhotoFolderID']
        VideoFolderID = config['Parameter']['VideoFolderID']
    else:
        CreateParameter()

def SaveParameter():
    #Parameter
    global VibrationWarningValue
    global VibrationAlarmValue
    global FireWarningTempValue
    global FireWarningCountValue
    global FireAlarmTempValue
    global FireAlarmCountValue
    global CapturePictureRH
    global CapturePictureRV
    global CaptureVideoSecond
    global SensorsFValue
    global CameraFValue
    global UpdateFValue
    global PhotoFolderID
    global VideoFolderID

    filePathString = "/home/pi/Parameter/Parameter.ini"
    if os.path.isfile(filePathString):
        config = configparser.ConfigParser()
        config.read(filePathString)
        config['Parameter']['VibrationWarningValue'] = str(VibrationWarningValue)
        config['Parameter']['VibrationAlarmValue'] = str(VibrationAlarmValue)
        config['Parameter']['FireWarningTempValue'] = str(FireWarningTempValue)
        config['Parameter']['FireWarningCountValue'] = str(FireWarningCountValue)
        config['Parameter']['FireAlarmTempValue'] = str(FireAlarmTempValue)
        config['Parameter']['FireAlarmCountValue'] = str(FireAlarmCountValue)
        config['Parameter']['CapturePictureRH'] = str(CapturePictureRH)
        config['Parameter']['CapturePictureRV'] = str(CapturePictureRV)
        config['Parameter']['CaptureVideoSecond'] = str(CaptureVideoSecond)
        config['Parameter']['SensorsFValue'] = str(SensorsFValue)
        config['Parameter']['CameraFValue'] = str(CameraFValue)
        config['Parameter']['UpdateFValue'] = str(UpdateFValue)
        config['Parameter']['PhotoFolderID'] = PhotoFolderID
        config['Parameter']['VideoFolderID'] = VideoFolderID

        with open(filePathString, 'w') as configfile:
            config.write(configfile)
    else:
        CreateParameter()

#endregion

#DIO function
#region DIO function

def DIO_Initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rled, GPIO.OUT)
    GPIO.setup(gled, GPIO.OUT)
    GPIO.output(rled, GPIO.OUT)

def DIO_Green(flag=True):
    if flag:
        GPIO.output(gled, GPIO.HIGH)
    else:
        GPIO.output(gled, GPIO.LOW)

def DIO_Finish():
    GPIO.cleanup()


#endregion


