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

class APIParameterDto:
    IsDataPlatformConnected=0
    Token = ''
    UseCloud = 0
    UserToken = ''
    CloudType = 0
    CloudUrl = ''


    def __init__(self):
        pass

class ParameterDataDto:
    GeneralParameter = None
    APIParameter = None

    def __init__(self) -> None:

        self.GeneralParameter = GeneralParameterDto()
        self.APIParameter = APIParameterDto()

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
        config['Parameter']['VibrationWarningValue'] = str(ParameterData.GeneralParameter.VibrationWarningValue)
        config['Parameter']['VibrationAlarmValue'] = str(ParameterData.GeneralParameter.VibrationAlarmValue)
        config['Parameter']['FireWarningTempValue'] = str(ParameterData.GeneralParameter.FireWarningTempValue)
        config['Parameter']['FireWarningCountValue'] = str(ParameterData.GeneralParameter.FireWarningCountValue)
        config['Parameter']['FireAlarmTempValue'] = str(ParameterData.GeneralParameter.FireAlarmTempValue)
        config['Parameter']['FireAlarmCountValue'] = str(ParameterData.GeneralParameter.FireAlarmCountValue)
        config['Parameter']['CapturePictureRH'] = str(ParameterData.GeneralParameter.CapturePictureRH)
        config['Parameter']['CapturePictureRV'] = str(ParameterData.GeneralParameter.CapturePictureRV)
        config['Parameter']['CaptureVideoSecond'] = str(ParameterData.GeneralParameter.CaptureVideoSecond)
        config['Parameter']['SensorsFValue'] = str(ParameterData.GeneralParameter.SensorsFValue)
        config['Parameter']['CameraFValue'] = str(ParameterData.GeneralParameter.CameraFValue)
        config['Parameter']['UpdateFValue'] = str(ParameterData.GeneralParameter.UpdateFValue)
        config['Parameter']['PhotoFolderID'] = ParameterData.GeneralParameter.PhotoFolderID
        config['Parameter']['VideoFolderID'] = ParameterData.GeneralParameter.VideoFolderID
        config['Parameter']['CameraFunction'] = str(ParameterData.GeneralParameter.CameraFunctionFlag)

        config['Parameter']['IsDataPlatformConnected']=str(ParameterData.APIParameter.IsDataPlatformConnected)
        config['Parameter']['Token']=ParameterData.APIParameter.Token
        config['Parameter']['UseCloud']=str(ParameterData.APIParameter.UseCloud)
        config['Parameter']['UserToken']=ParameterData.APIParameter.UserToken
        config['Parameter']['CloudType']=str(ParameterData.APIParameter.CloudType)
        config['Parameter']['CloudUrl']=ParameterData.APIParameter.CloudUrl


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
                ParameterData.GeneralParameter.VibrationWarningValue = config['Parameter'].getfloat('VibrationWarningValue')
                ParameterData.GeneralParameter.VibrationAlarmValue = config['Parameter'].getfloat('VibrationAlarmValue')
                ParameterData.GeneralParameter.FireWarningTempValue = config['Parameter'].getfloat('FireWarningTempValue')
                ParameterData.GeneralParameter.FireWarningCountValue = config['Parameter'].getint('FireWarningCountValue')
                ParameterData.GeneralParameter.FireAlarmTempValue = config['Parameter'].getfloat('FireAlarmTempValue')
                ParameterData.GeneralParameter.FireAlarmCountValue = config['Parameter'].getint('FireAlarmCountValue')
                ParameterData.GeneralParameter.CapturePictureRH = config['Parameter'].getint('CapturePictureRH')
                ParameterData.GeneralParameter.CapturePictureRV = config['Parameter'].getint('CapturePictureRV')
                ParameterData.GeneralParameter.CaptureVideoSecond = config['Parameter'].getint('CaptureVideoSecond')
                ParameterData.GeneralParameter.SensorsFValue = config['Parameter'].getfloat('SensorsFValue')
                ParameterData.GeneralParameter.CameraFValue = config['Parameter'].getfloat('CameraFValue')
                ParameterData.GeneralParameter.UpdateFValue = config['Parameter'].getfloat('UpdateFValue')
                ParameterData.GeneralParameter.PhotoFolderID = config['Parameter'].get('PhotoFolderID')
                ParameterData.GeneralParameter.VideoFolderID = config['Parameter'].get('VideoFolderID')
                ParameterData.GeneralParameter.CameraFunctionFlag = config['Parameter'].getint('CameraFunction')

                checkExist = config['Parameter'].getint('IsDataPlatformConnected', -1)
                if checkExist == -1:
                    self.SaveParameter()
                else:
                    ParameterData.APIParameter.IsDataPlatformConnected=config['Parameter'].getint('IsDataPlatformConnected')
                    ParameterData.APIParameter.Token=config['Parameter'].get('Token')
                    ParameterData.APIParameter.UseCloud=config['Parameter'].getint('UseCloud')
                    ParameterData.APIParameter.UserToken=config['Parameter'].get('UserToken')
                    ParameterData.APIParameter.CloudType=config['Parameter'].getint('CloudType')
                    ParameterData.APIParameter.CloudUrl=config['Parameter'].get('CloudUrl')

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
                config['Parameter']['VibrationWarningValue'] = str(ParameterData.GeneralParameter.VibrationWarningValue)
                config['Parameter']['VibrationAlarmValue'] = str(ParameterData.GeneralParameter.VibrationAlarmValue)
                config['Parameter']['FireWarningTempValue'] = str(ParameterData.GeneralParameter.FireWarningTempValue)
                config['Parameter']['FireWarningCountValue'] = str(ParameterData.GeneralParameter.FireWarningCountValue)
                config['Parameter']['FireAlarmTempValue'] = str(ParameterData.GeneralParameter.FireAlarmTempValue)
                config['Parameter']['FireAlarmCountValue'] = str(ParameterData.GeneralParameter.FireAlarmCountValue)
                config['Parameter']['CapturePictureRH'] = str(ParameterData.GeneralParameter.CapturePictureRH)
                config['Parameter']['CapturePictureRV'] = str(ParameterData.GeneralParameter.CapturePictureRV)
                config['Parameter']['CaptureVideoSecond'] = str(ParameterData.GeneralParameter.CaptureVideoSecond)
                config['Parameter']['SensorsFValue'] = str(ParameterData.GeneralParameter.SensorsFValue)
                config['Parameter']['CameraFValue'] = str(ParameterData.GeneralParameter.CameraFValue)
                config['Parameter']['UpdateFValue'] = str(ParameterData.GeneralParameter.UpdateFValue)
                config['Parameter']['PhotoFolderID'] = ParameterData.GeneralParameter.PhotoFolderID
                config['Parameter']['VideoFolderID'] = ParameterData.GeneralParameter.VideoFolderID
                config['Parameter']['CameraFunction'] = str(ParameterData.GeneralParameter.CameraFunctionFlag)

                config['Parameter']['IsDataPlatformConnected']=str(ParameterData.APIParameter.IsDataPlatformConnected)
                config['Parameter']['Token']=ParameterData.APIParameter.Token
                config['Parameter']['UseCloud']=str(ParameterData.APIParameter.UseCloud)
                config['Parameter']['UserToken']=ParameterData.APIParameter.UserToken
                config['Parameter']['CloudType']=str(ParameterData.APIParameter.CloudType)
                config['Parameter']['CloudUrl']=ParameterData.APIParameter.CloudUrl


                with open(filePathString, 'w') as configfile:
                    config.write(configfile)
            else:
                self.CreateParameter()


            MyPrint.Print_Green('Save Parameter Success => ' + filePathString,ParameterInfoString)
                
        except:
            MyPrint.Print_Red('Save Parameter Failure => ' + filePathString, ParameterErrorString)


        
ParameterOPInstance = ParameterOperator()

