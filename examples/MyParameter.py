#!/usr/bin/python3
#MyParameter.py
import os
import configparser
import RPi.GPIO as GPIO

sSoftwareVersion='1.0.2.0'

#API
IsDataPlatformConnected=False
Token=""
UseCloud=False
UserToken=""
CloudType=0
CloudUrl=""


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
CameraFunctionFlag=0

rled=24
gled=23

C_ISO = 400
C_ShutterSpeed=3000
C_Rotation=0

C_OD_Funciton=0
C_OD_X1=0
C_OD_Y1=0
C_OD_X2=0
C_OD_Y2=0
C_EF_Function=0
C_EF_X1=0
C_EF_X2=0

C_OD_G_Mean=0.0
C_OD_G_Light=0.0
C_OD_G_R=0.0
C_OD_G_G=0.0
C_OD_G_B=0.0

C_Image_Update_API=''
C_Video_Update_API=''


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
    global CameraFunctionFlag

    global C_ISO
    global C_ShutterSpeed
    global C_Rotation
    global C_OD_Funciton
    global C_OD_X1
    global C_OD_Y1
    global C_OD_X2
    global C_OD_Y2
    global C_EF_Function
    global C_EF_X1
    global C_EF_X2

    global C_OD_G_Mean
    global C_OD_G_Light
    global C_OD_G_R
    global C_OD_G_G
    global C_OD_G_B

    if not os.path.isdir("/home/pi/Parameter/"):
        os.mkdir("/home/pi/Parameter/")
    filePathString = "/home/pi/Parameter/Parameter.ini"
    filePathString2 = "/home/pi/Parameter/CameraParameter.ini"

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
    config['Parameter']['CameraFunction'] = str(CameraFunctionFlag)

    config2 = configparser.ConfigParser()
    config2['CameraSetting']={}
    config2['CameraSetting']['Parameter01'] = str(C_ISO)
    config2['CameraSetting']['Parameter02'] = str(C_ShutterSpeed)
    config2['CameraSetting']['Parameter03'] = str(C_Rotation)
    config2['CameraSetting']['Parameter04'] = '0'
    config2['CameraSetting']['Parameter05'] = '0'
    config2['CameraSetting']['Parameter06'] = '0'
    config2['CameraSetting']['Parameter07'] = '0'
    config2['CameraSetting']['Parameter08'] = '0'
    config2['CameraSetting']['Parameter09'] = '0'
    config2['CameraSetting']['Parameter10'] = '0'
    config2['CameraIgnition']['Parameter01']=str(C_OD_Funciton)
    config2['CameraIgnition']['Parameter02']=str(C_OD_X1)
    config2['CameraIgnition']['Parameter03']=str(C_OD_Y1)
    config2['CameraIgnition']['Parameter04']=str(C_OD_X2)
    config2['CameraIgnition']['Parameter05']=str(C_OD_Y2)
    config2['CameraIgnition']['Parameter06']=str(C_EF_Function)
    config2['CameraIgnition']['Parameter07']=str(C_EF_X1)
    config2['CameraIgnition']['Parameter08']=str(C_EF_X2)
    config2['CameraIgnition']['Parameter09']='0'
    config2['CameraIgnition']['Parameter10']='0'
    config2['CameraIgnition']['Parameter11']='0'
    config2['CameraIgnition']['Parameter12']='0'
    config2['CameraIgnition']['Parameter13']='0'
    config2['CameraIgnition']['Parameter14']='0'
    config2['CameraIgnition']['Parameter15']='0'
    config2['CameraIgnition']['Parameter16']='0'
    config2['CameraIgnition']['Parameter17']='0'
    config2['CameraIgnition']['Parameter18']='0'
    config2['CameraIgnition']['Parameter19']='0'
    config2['CameraIgnition']['Parameter20']='0'

    with open(filePathString, 'w') as configfile:
        config.write(configfile)

    with open(filePathString2, 'w') as configfile2:
        config2.write(configfile2)

def CreateParameter2():
    #Parameter
    global C_ISO
    global C_ShutterSpeed
    global C_Rotation
    global C_OD_Funciton
    global C_OD_X1
    global C_OD_Y1
    global C_OD_X2
    global C_OD_Y2
    global C_EF_Function
    global C_EF_X1
    global C_EF_X2

    global C_OD_G_Mean
    global C_OD_G_Light
    global C_OD_G_R
    global C_OD_G_G
    global C_OD_G_B

    global C_Image_Update_API
    global C_Video_Update_API

    if not os.path.isdir("/home/pi/Parameter/"):
        os.mkdir("/home/pi/Parameter/")
    filePathString2 = "/home/pi/Parameter/CameraParameter.ini"

    config2 = configparser.ConfigParser()
    config2['CameraSetting']={}
    config2['CameraSetting']['Parameter01'] = str(C_ISO)
    config2['CameraSetting']['Parameter02'] = str(C_ShutterSpeed)
    config2['CameraSetting']['Parameter03'] = str(C_Rotation)
    config2['CameraSetting']['Parameter04'] = str(C_Image_Update_API)
    config2['CameraSetting']['Parameter05'] = str(C_Video_Update_API)
    config2['CameraSetting']['Parameter06'] = '0'
    config2['CameraSetting']['Parameter07'] = '0'
    config2['CameraSetting']['Parameter08'] = '0'
    config2['CameraSetting']['Parameter09'] = '0'
    config2['CameraSetting']['Parameter10'] = '0'
    config2['CameraIgnition']={}
    config2['CameraIgnition']['Parameter01']=str(C_OD_Funciton)
    config2['CameraIgnition']['Parameter02']=str(C_OD_X1)
    config2['CameraIgnition']['Parameter03']=str(C_OD_Y1)
    config2['CameraIgnition']['Parameter04']=str(C_OD_X2)
    config2['CameraIgnition']['Parameter05']=str(C_OD_Y2)
    config2['CameraIgnition']['Parameter06']=str(C_EF_Function)
    config2['CameraIgnition']['Parameter07']=str(C_EF_X1)
    config2['CameraIgnition']['Parameter08']=str(C_EF_X2)
    config2['CameraIgnition']['Parameter09']=str(C_OD_G_Mean)
    config2['CameraIgnition']['Parameter10']=str(C_OD_G_Light)
    config2['CameraIgnition']['Parameter11']=str(C_OD_G_R)
    config2['CameraIgnition']['Parameter12']=str(C_OD_G_G)
    config2['CameraIgnition']['Parameter13']=str(C_OD_G_B)
    config2['CameraIgnition']['Parameter14']='0'
    config2['CameraIgnition']['Parameter15']='0'
    config2['CameraIgnition']['Parameter16']='0'
    config2['CameraIgnition']['Parameter17']='0'
    config2['CameraIgnition']['Parameter18']='0'
    config2['CameraIgnition']['Parameter19']='0'
    config2['CameraIgnition']['Parameter20']='0'

    with open(filePathString2, 'w') as configfile2:
        config2.write(configfile2)

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
    global CameraFunctionFlag

    global C_ISO
    global C_ShutterSpeed
    global C_Rotation
    global C_OD_Funciton
    global C_OD_X1
    global C_OD_Y1
    global C_OD_X2
    global C_OD_Y2
    global C_EF_Function
    global C_EF_X1
    global C_EF_X2

    global C_OD_G_Mean
    global C_OD_G_Light
    global C_OD_G_R
    global C_OD_G_G
    global C_OD_G_B

    global C_Image_Update_API
    global C_Video_Update_API

    filePathString = "/home/pi/Parameter/Parameter.ini"
    filePathString2 = "/home/pi/Parameter/CameraParameter.ini"

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
        CameraFunctionFlag = config['Parameter'].getint('CameraFunction')
    else:
        CreateParameter()

    if os.path.isfile(filePathString2):
        config2 = configparser.ConfigParser()
        config2.read(filePathString2)
        C_ISO = config2['CameraSetting'].getint('Parameter01')
        C_ShutterSpeed = config2['CameraSetting'].getint('Parameter02')
        C_Rotation = config2['CameraSetting'].getint('Parameter03')
        C_Image_Update_API = str(config2['CameraSetting'].get('Parameter04'))
        C_Video_Update_API = str(config2['CameraSetting'].get('Parameter05'))
        C_OD_Funciton = config2['CameraIgnition'].getint('Parameter01')
        C_OD_X1 = config2['CameraIgnition'].getint('Parameter02')
        C_OD_Y1 = config2['CameraIgnition'].getint('Parameter03')
        C_OD_X2 = config2['CameraIgnition'].getint('Parameter04')
        C_OD_Y2 = config2['CameraIgnition'].getint('Parameter05')
        C_EF_Function = config2['CameraIgnition'].getint('Parameter06')
        C_EF_X1 = config2['CameraIgnition'].getint('Parameter07')
        C_EF_X2 = config2['CameraIgnition'].getint('Parameter08')
        C_OD_G_Mean = config2['CameraIgnition'].getfloat('Parameter09')
        C_OD_G_Light = config2['CameraIgnition'].getfloat('Parameter10')
        C_OD_G_R = config2['CameraIgnition'].getfloat('Parameter11')
        C_OD_G_G = config2['CameraIgnition'].getfloat('Parameter12')
        C_OD_G_B = config2['CameraIgnition'].getfloat('Parameter13')
    else:
        CreateParameter2()

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
    global CameraFunctionFlag

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
        config['Parameter']['CameraFunction'] = str(CameraFunctionFlag)

        with open(filePathString, 'w') as configfile:
            config.write(configfile)
    else:
        CreateParameter()

def SaveParameter2():
    #Parameter
    global C_ISO
    global C_ShutterSpeed
    global C_Rotation
    global C_OD_Funciton
    global C_OD_X1
    global C_OD_Y1
    global C_OD_X2
    global C_OD_Y2
    global C_EF_Function
    global C_EF_X1
    global C_EF_X2

    global C_OD_G_Mean
    global C_OD_G_Light
    global C_OD_G_R
    global C_OD_G_G
    global C_OD_G_B

    global C_Image_Update_API
    global C_Video_Update_API

    filePathString2 = "/home/pi/Parameter/CameraParameter.ini"
    if os.path.isfile(filePathString2):
        config2 = configparser.ConfigParser()
        config2['CameraSetting']={}
        config2['CameraSetting']['Parameter01'] = str(C_ISO)
        config2['CameraSetting']['Parameter02'] = str(C_ShutterSpeed)
        config2['CameraSetting']['Parameter03'] = str(C_Rotation)
        config2['CameraSetting']['Parameter04'] = str(C_Image_Update_API)
        config2['CameraSetting']['Parameter05'] = str(C_Video_Update_API)
        config2['CameraSetting']['Parameter06'] = '0'
        config2['CameraSetting']['Parameter07'] = '0'
        config2['CameraSetting']['Parameter08'] = '0'
        config2['CameraSetting']['Parameter09'] = '0'
        config2['CameraSetting']['Parameter10'] = '0'
        config2['CameraIgnition']={}
        config2['CameraIgnition']['Parameter01']=str(C_OD_Funciton)
        config2['CameraIgnition']['Parameter02']=str(C_OD_X1)
        config2['CameraIgnition']['Parameter03']=str(C_OD_Y1)
        config2['CameraIgnition']['Parameter04']=str(C_OD_X2)
        config2['CameraIgnition']['Parameter05']=str(C_OD_Y2)
        config2['CameraIgnition']['Parameter06']=str(C_EF_Function)
        config2['CameraIgnition']['Parameter07']=str(C_EF_X1)
        config2['CameraIgnition']['Parameter08']=str(C_EF_X2)
        config2['CameraIgnition']['Parameter09']=str(C_OD_G_Mean)
        config2['CameraIgnition']['Parameter10']=str(C_OD_G_Light)
        config2['CameraIgnition']['Parameter11']=str(C_OD_G_R)
        config2['CameraIgnition']['Parameter12']=str(C_OD_G_G)
        config2['CameraIgnition']['Parameter13']=str(C_OD_G_B)
        config2['CameraIgnition']['Parameter14']='0'
        config2['CameraIgnition']['Parameter15']='0'
        config2['CameraIgnition']['Parameter16']='0'
        config2['CameraIgnition']['Parameter17']='0'
        config2['CameraIgnition']['Parameter18']='0'
        config2['CameraIgnition']['Parameter19']='0'
        config2['CameraIgnition']['Parameter20']='0'

        with open(filePathString2, 'w') as configfile2:
            config2.write(configfile2)
    else:
        CreateParameter2()

#endregion

#DIO function
#region DIO function

def DIO_Initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rled, GPIO.OUT)
    GPIO.setup(gled, GPIO.OUT)
    GPIO.output(rled, GPIO.HIGH)

def DIO_Green(flag=True):
    if flag:
        GPIO.output(gled, GPIO.HIGH)
    else:
        GPIO.output(gled, GPIO.LOW)

def DIO_Finish():
    GPIO.output(rled, GPIO.LOW)
    GPIO.output(gled, GPIO.LOW)
    GPIO.cleanup()


#endregion


