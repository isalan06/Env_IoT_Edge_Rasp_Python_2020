#!/usr/bin/python3
#MyParameterOperator.py
import os
import configparser
import MyPrint

ParameterInfoString = 'Parameter Info'
ParameterErrorString = 'Parameter Info'

class GeneralParameterDto:
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

    def __init__(self) -> None:
        pass

class ParameterDataDto:
    GeneralParameter = None

    def __init__(self) -> None:

        self.GeneralParameter = GeneralParameterDto()

ParameterData = ParameterDataDto()

TargetPath = "/home/pi/Parameter/V2_0/"
GeneralFileName = "Parameter.ini"

class ParameterOperator:
    global TargetPath
    global GeneralFileName


    def __init__(self) -> None:
        pass

    def CreateParameter(self):
        global ParameterData

        if not os.path.isdir(TargetPath):
            os.mkdir(TargetPath)
        filePathString = TargetPath + GeneralFileName

        #region General Parameter

        config = configparser.ConfigParser()
        config['Parameter'] = {} 
        config['Parameter']['VibrationWarningValue'] = str(ParameterData.VibrationWarningValue)
        config['Parameter']['VibrationAlarmValue'] = str(ParameterData.VibrationAlarmValue)
        config['Parameter']['FireWarningTempValue'] = str(ParameterData.FireWarningTempValue)
        config['Parameter']['FireWarningCountValue'] = str(ParameterData.FireWarningCountValue)
        config['Parameter']['FireAlarmTempValue'] = str(ParameterData.FireAlarmTempValue)
        config['Parameter']['FireAlarmCountValue'] = str(ParameterData.FireAlarmCountValue)
        config['Parameter']['CapturePictureRH'] = str(ParameterData.CapturePictureRH)
        config['Parameter']['CapturePictureRV'] = str(ParameterData.CapturePictureRV)
        config['Parameter']['CaptureVideoSecond'] = str(ParameterData.CaptureVideoSecond)
        config['Parameter']['SensorsFValue'] = str(ParameterData.SensorsFValue)
        config['Parameter']['CameraFValue'] = str(ParameterData.CameraFValue)
        config['Parameter']['UpdateFValue'] = str(ParameterData.UpdateFValue)
        config['Parameter']['PhotoFolderID'] = ParameterData.PhotoFolderID
        config['Parameter']['VideoFolderID'] = ParameterData.VideoFolderID
        config['Parameter']['CameraFunction'] = str(ParameterData.CameraFunctionFlag)

        try:
            with open(filePathString, 'w') as configfile:
                config.write(configfile)
            MyPrint.Print_Green('Create Parameter Success => ' + filePathString,ParameterInfoString)
        except Exception as e:
            MyPrint.Print_Red('Create Parameter Failure => ' + filePathString,ParameterErrorString)
            print(e)

        #endregion

    def LoadParameter(self):
        global ParameterData
        global TargetPath
        global GeneralFileName

        filePathString = TargetPath + GeneralFileName

        try:
            if os.path.isfile(filePathString):
                config = configparser.ConfigParser()
                config.read(filePathString)
                ParameterData.VibrationWarningValue = config['Parameter'].getfloat('VibrationWarningValue')
                ParameterData.VibrationAlarmValue = config['Parameter'].getfloat('VibrationAlarmValue')
                ParameterData.FireWarningTempValue = config['Parameter'].getfloat('FireWarningTempValue')
                ParameterData.FireWarningCountValue = config['Parameter'].getint('FireWarningCountValue')
                ParameterData.FireAlarmTempValue = config['Parameter'].getfloat('FireAlarmTempValue')
                ParameterData.FireAlarmCountValue = config['Parameter'].getint('FireAlarmCountValue')
                ParameterData.CapturePictureRH = config['Parameter'].getint('CapturePictureRH')
                ParameterData.CapturePictureRV = config['Parameter'].getint('CapturePictureRV')
                ParameterData.CaptureVideoSecond = config['Parameter'].getint('CaptureVideoSecond')
                ParameterData.SensorsFValue = config['Parameter'].getfloat('SensorsFValue')
                ParameterData.CameraFValue = config['Parameter'].getfloat('CameraFValue')
                ParameterData.UpdateFValue = config['Parameter'].getfloat('UpdateFValue')
                ParameterData.PhotoFolderID = config['Parameter'].get('PhotoFolderID')
                ParameterData.VideoFolderID = config['Parameter'].get('VideoFolderID')
                ParameterData.CameraFunctionFlag = config['Parameter'].getint('CameraFunction')

                MyPrint.Print_Green('Load Parameter Success => ' + filePathString,ParameterInfoString)
            else:
                self.CreateParameter()
                
        except Exception as e:
            MyPrint.Print_Red('Load Parameter Failure => ' + filePathString, ParameterErrorString)
            print(e)
        
    def SaveParameter(self):
        global ParameterData

        filePathString = self.TargetPath + self.GeneralFileName

        try:
            if os.path.isfile(filePathString):
                config = configparser.ConfigParser()
                config.read(filePathString)
                config['Parameter']['VibrationWarningValue'] = str(ParameterData.VibrationWarningValue)
                config['Parameter']['VibrationAlarmValue'] = str(ParameterData.VibrationAlarmValue)
                config['Parameter']['FireWarningTempValue'] = str(ParameterData.FireWarningTempValue)
                config['Parameter']['FireWarningCountValue'] = str(ParameterData.FireWarningCountValue)
                config['Parameter']['FireAlarmTempValue'] = str(ParameterData.FireAlarmTempValue)
                config['Parameter']['FireAlarmCountValue'] = str(ParameterData.FireAlarmCountValue)
                config['Parameter']['CapturePictureRH'] = str(ParameterData.CapturePictureRH)
                config['Parameter']['CapturePictureRV'] = str(ParameterData.CapturePictureRV)
                config['Parameter']['CaptureVideoSecond'] = str(ParameterData.CaptureVideoSecond)
                config['Parameter']['SensorsFValue'] = str(ParameterData.SensorsFValue)
                config['Parameter']['CameraFValue'] = str(ParameterData.CameraFValue)
                config['Parameter']['UpdateFValue'] = str(ParameterData.UpdateFValue)
                config['Parameter']['PhotoFolderID'] = ParameterData.PhotoFolderID
                config['Parameter']['VideoFolderID'] = ParameterData.VideoFolderID
                config['Parameter']['CameraFunction'] = str(ParameterData.CameraFunctionFlag)


                with open(filePathString, 'w') as configfile:
                    config.write(configfile)
            else:
                self.CreateParameter()


            MyPrint.Print_Green('Save Parameter Success => ' + filePathString,ParameterInfoString)
                
        except:
            MyPrint.Print_Red('Save Parameter Failure => ' + filePathString, ParameterErrorString)


        
ParameterOPInstance = ParameterOperator()

