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

class ImageParameterDto:
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

    def __init__(self) -> None:
        pass

class ParameterDataDto:
    GeneralParameter = None
    APIParameter = None
    ImageParameter = None

    def __init__(self) -> None:

        self.GeneralParameter = GeneralParameterDto()
        self.APIParameter = APIParameterDto()
        self.ImageParameter = ImageParameterDto()

ParameterData = ParameterDataDto()

TargetPath = "/home/pi/Parameter/V2_0/"
GeneralFileName = "Parameter.ini"
ImageFileName = "CameraParameter.ini"

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

    def CreateParameter2(self):
        global ParameterData

        print('Create Parameter 2')

        if not os.path.isdir(TargetPath):
            os.mkdir(TargetPath)
        filePathString2 = TargetPath + ImageFileName

        try:

            config2 = configparser.ConfigParser()
            config2['CameraSetting']={}
            config2['CameraSetting']['Parameter01'] = str(ParameterData.ImageParameter.C_ISO)
            config2['CameraSetting']['Parameter02'] = str(ParameterData.ImageParameter.C_ShutterSpeed)
            config2['CameraSetting']['Parameter03'] = str(ParameterData.ImageParameter.C_Rotation)
            config2['CameraSetting']['Parameter04'] = ParameterData.ImageParameter.C_Image_Update_API
            config2['CameraSetting']['Parameter05'] = ParameterData.ImageParameter.C_Video_Update_API
            config2['CameraSetting']['Parameter06'] = '0'
            config2['CameraSetting']['Parameter07'] = '0'
            config2['CameraSetting']['Parameter08'] = '0'
            config2['CameraSetting']['Parameter09'] = '0'
            config2['CameraSetting']['Parameter10'] = '0'
            config2['CameraIgnition']={}
            config2['CameraIgnition']['Parameter01']=str(ParameterData.ImageParameter.C_OD_Funciton)
            config2['CameraIgnition']['Parameter02']=str(ParameterData.ImageParameter.C_OD_X1)
            config2['CameraIgnition']['Parameter03']=str(ParameterData.ImageParameter.C_OD_Y1)
            config2['CameraIgnition']['Parameter04']=str(ParameterData.ImageParameter.C_OD_X2)
            config2['CameraIgnition']['Parameter05']=str(ParameterData.ImageParameter.C_OD_Y2)
            config2['CameraIgnition']['Parameter06']=str(ParameterData.ImageParameter.C_EF_Function)
            config2['CameraIgnition']['Parameter07']=str(ParameterData.ImageParameter.C_EF_X1)
            config2['CameraIgnition']['Parameter08']=str(ParameterData.ImageParameter.C_EF_X2)
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
        except Exception as e:
            MyPrint.Print_Red('Create Parameter Failure 2 => ' + filePathString2,ParameterErrorString)
            print(e)

        try:
            with open(filePathString2, 'w') as configfile2:
                config2.write(configfile2)
            MyPrint.Print_Green('Create Parameter Success => ' + filePathString2,ParameterInfoString)
        except Exception as e:
            MyPrint.Print_Red('Create Parameter Failure => ' + filePathString2,ParameterErrorString)
            print(e)

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

    def LoadParameter2(self):
        global ParameterData

        filePathString2 = TargetPath + ImageFileName

        try:
            if os.path.isfile(filePathString2):
                config2 = configparser.ConfigParser()
                config2.read(filePathString2)

                print('load parameter2')

                ParameterData.ImageParameter.C_ISO = config2['CameraSetting'].getint('Parameter01')
                ParameterData.ImageParameter.C_ShutterSpeed = config2['CameraSetting'].getint('Parameter02')
                ParameterData.ImageParameter.C_Rotation = config2['CameraSetting'].getint('Parameter03')
                ParameterData.ImageParameter.C_Image_Update_API = str(config2['CameraSetting'].get('Parameter04'))
                ParameterData.ImageParameter.C_Video_Update_API = str(config2['CameraSetting'].get('Parameter05'))
                ParameterData.ImageParameter.C_OD_Funciton = config2['CameraIgnition'].getint('Parameter01')
                ParameterData.ImageParameter.C_OD_X1 = config2['CameraIgnition'].getint('Parameter02')
                ParameterData.ImageParameter.C_OD_Y1 = config2['CameraIgnition'].getint('Parameter03')
                ParameterData.ImageParameter.C_OD_X2 = config2['CameraIgnition'].getint('Parameter04')
                ParameterData.ImageParameter.C_OD_Y2 = config2['CameraIgnition'].getint('Parameter05')
                ParameterData.ImageParameter.C_EF_Function = config2['CameraIgnition'].getint('Parameter06')
                ParameterData.ImageParameter.C_EF_X1 = config2['CameraIgnition'].getint('Parameter07')
                ParameterData.ImageParameter.C_EF_X2 = config2['CameraIgnition'].getint('Parameter08')
                ParameterData.ImageParameter.C_OD_G_Mean = config2['CameraIgnition'].getfloat('Parameter09')
                ParameterData.ImageParameter.C_OD_G_Light = config2['CameraIgnition'].getfloat('Parameter10')
                ParameterData.ImageParameter.C_OD_G_R = config2['CameraIgnition'].getfloat('Parameter11')
                ParameterData.ImageParameter.C_OD_G_G = config2['CameraIgnition'].getfloat('Parameter12')
                ParameterData.ImageParameter.C_OD_G_B = config2['CameraIgnition'].getfloat('Parameter13')

                MyPrint.Print_Green('Load Parameter Success => ' + filePathString2, ParameterInfoString)
            else:
                self.CreateParameter2()
                
        except Exception as e:
            MyPrint.Print_Red('Load Parameter Failure => ' + filePathString2, ParameterErrorString)
            print(e)
        
    def SaveParameter(self):
        global ParameterData


        filePathString = TargetPath + GeneralFileName

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

    def SaveParameter2(self):
        global ParameterData

        filePathString2 = TargetPath + ImageFileName

        try:
            if os.path.isfile(filePathString2):
                config2 = configparser.ConfigParser()
                config2.read(filePathString2)
                config2['CameraSetting']={}
                config2['CameraSetting']['Parameter01'] = str(ParameterData.ImageParameter.C_ISO)
                config2['CameraSetting']['Parameter02'] = str(ParameterData.ImageParameter.C_ShutterSpeed)
                config2['CameraSetting']['Parameter03'] = str(ParameterData.ImageParameter.C_Rotation)
                config2['CameraSetting']['Parameter04'] = str(ParameterData.ImageParameter.C_Image_Update_API)
                config2['CameraSetting']['Parameter05'] = str(ParameterData.ImageParameter.C_Video_Update_API)
                config2['CameraSetting']['Parameter06'] = '0'
                config2['CameraSetting']['Parameter07'] = '0'
                config2['CameraSetting']['Parameter08'] = '0'
                config2['CameraSetting']['Parameter09'] = '0'
                config2['CameraSetting']['Parameter10'] = '0'
                config2['CameraIgnition']={}
                config2['CameraIgnition']['Parameter01']=str(ParameterData.ImageParameter.C_OD_Funciton)
                config2['CameraIgnition']['Parameter02']=str(ParameterData.ImageParameter.C_OD_X1)
                config2['CameraIgnition']['Parameter03']=str(ParameterData.ImageParameter.C_OD_Y1)
                config2['CameraIgnition']['Parameter04']=str(ParameterData.ImageParameter.C_OD_X2)
                config2['CameraIgnition']['Parameter05']=str(ParameterData.ImageParameter.C_OD_Y2)
                config2['CameraIgnition']['Parameter06']=str(ParameterData.ImageParameter.C_EF_Function)
                config2['CameraIgnition']['Parameter07']=str(ParameterData.ImageParameter.C_EF_X1)
                config2['CameraIgnition']['Parameter08']=str(ParameterData.ImageParameter.C_EF_X2)
                config2['CameraIgnition']['Parameter09']=str(ParameterData.ImageParameter.C_OD_G_Mean)
                config2['CameraIgnition']['Parameter10']=str(ParameterData.ImageParameter.C_OD_G_Light)
                config2['CameraIgnition']['Parameter11']=str(ParameterData.ImageParameter.C_OD_G_R)
                config2['CameraIgnition']['Parameter12']=str(ParameterData.ImageParameter.C_OD_G_G)
                config2['CameraIgnition']['Parameter13']=str(ParameterData.ImageParameter.C_OD_G_B)
                config2['CameraIgnition']['Parameter14']='0'
                config2['CameraIgnition']['Parameter15']='0'
                config2['CameraIgnition']['Parameter16']='0'
                config2['CameraIgnition']['Parameter17']='0'
                config2['CameraIgnition']['Parameter18']='0'
                config2['CameraIgnition']['Parameter19']='0'
                config2['CameraIgnition']['Parameter20']='0'


                with open(filePathString2, 'w') as configfile:
                    config2.write(configfile)
            else:
                self.CreateParameter2()


            MyPrint.Print_Green('Save Parameter Success => ' + filePathString2,ParameterInfoString)
                
        except:
            MyPrint.Print_Red('Save Parameter Failure => ' + filePathString2, ParameterErrorString)


        
ParameterOPInstance = ParameterOperator()

