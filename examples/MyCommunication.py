#!/usr/bin/python3
#MyCommunication.py

from pathlib import Path
import MyParameter
import MyCamera

import json
import requests
import os
import ssl
import time

sSoftwareVersion='1.1.0.1'


basicUrl='http://211.75.141.1:40080/Gateway'
_macaddress=''

tCheckTimer_Start = time.time()
tCheckTimer_CloudType0_Get = time.time()
tCheckTimer_CloudType0_Update =time.time()

sDHT22Status='Stop'
sThermalStatus='Stop'
sAccelGaugeStatus='Stop'
aSensorData={}
aParameter={}
aCameraParameter={}
aMachineOperation={}
aODParameter={}

aCloudType0UpdateData={}
bCloudType0UpdateTrigger=False

if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_BLUE = ''
    ANSI_MAGENTA = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_BLUE = ANSI_CSI + '1;34;40m'
    ANSI_MAGENTA = ANSI_CSI + '35m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'

def getMachineInformation(macaddress):

    global sSoftwareVersion
    global _macaddress
    global basicUrl

    _macaddress = macaddress

    print(ANSI_BLUE + '[Info] Start to get machine information from data platform!' + ANSI_OFF)

    requestData={}
    requestData['MacAddress']=_macaddress
    requestData['ProgramVersion']=MyParameter.sProgramSoftwareVersion
    requestData['ParameterVersion']=MyParameter.sSoftwareVersion
    requestData['CameraVersion']=MyParameter.sSoftwareVersion
    requestData['CommunicationVersion']=sSoftwareVersion
    requestData['CloudVersion']='NA'

    TransferJSONData=json.dumps(requestData)
    url = basicUrl + '/GetTokenByMacAddress'

    auth=('token', 'example')
    ssl._create_default_https_context = ssl._create_unverified_context
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.request("POST", url, headers=headers, data=TransferJSONData, timeout=10)
        data = response.json()
        
        print(data)
        result = data['result']
        if result==0:
            MyParameter.IsDataPlatformConnected=1
            MyParameter.Token = data['Token']
            MyParameter.UseCloud = 0 if (data['UseCloud'] == 0) else 1
            MyParameter.UserToken = data['UserToken']
            MyParameter.CloudUrl = data['CloudUrl']
            MyParameter.CloudType = data['CloudType']

            MyParameter.SaveParameter()
        elif result == 3:
            url = basicUrl + '/AddMacAddress'
            requestData['Location']=''
            requestData['UseCloud']=0
            requestData['CloudUrl']=''
            requestData['CloudType']=0
            requestData['UserToken']=''
            requestData['Longitude']=0
            requestData['Latitude']=0

            TransferJSONData=json.dumps(requestData)
            response = requests.request("POST", url, headers=headers, data=TransferJSONData, timeout=10)
            data = response.json()
            if result==0:
                MyParameter.IsDataPlatformConnected=True
                MyParameter.Token = data['Token']


        print(ANSI_BLUE + '[Info] Finish getting machine information from data platform!' + ANSI_OFF)
        if MyParameter.IsDataPlatformConnected:
            print(ANSI_BLUE + '[Info] Start to update data to data platform!' + ANSI_OFF)
        else:
            print(ANSI_RED + '[Error] Cannot update data to data platform' + ANSI_OFF)

                        
    except requests.exceptions.RequestException as e:
        print(ANSI_RED + '[Error] ' + str(e) + ANSI_OFF)

def UpdateMachineStatus(macaddress):
    global basicUrl

    _macaddress = macaddress
    auth=('token', 'example')
    ssl._create_default_https_context = ssl._create_unverified_context
    headers = {'Content-Type': 'application/json'}
    headers['Token']=MyParameter.Token
    requestData={}
    requestData['MacAddress']=_macaddress
    requestData['CameraStatus']=MyParameter.sCameraStatus
    if MyParameter.sCameraStatus == 'Running':
        if MyCamera.iSmallImageIndex == 0: 
            requestData['CameraSmallImage']=MyCamera.sSmallImageData
        if MyCamera.iSmallImageIndex == 1:
            requestData['CameraSmallImage']=MyCamera.sSmallImageData2
    
            
    requestData['DHT22Status']=sDHT22Status
    requestData['ThermalStatus']=sThermalStatus
    requestData['AccelGaugeStatus']=sAccelGaugeStatus
    requestData['SensorData']=aSensorData
    requestData['Parameter']=aParameter
    requestData['CameraParameter']=aCameraParameter
    requestData['MachineOperation']=aMachineOperation
    requestData['CloudParameter']={}
    requestData['CloudParameter']['UseCloud']=MyParameter.UseCloud
    requestData['CloudParameter']['UserToken']=MyParameter.UserToken
    requestData['CloudParameter']['CloudType']=MyParameter.CloudType
    requestData['CloudParameter']['CloudUrl']=MyParameter.CloudUrl
    requestData['ODParameter']=aODParameter
    
    #print(ANSI_GREEN + '[INFO] ' + str(requestData) + ANSI_OFF)
    TransferJSONData=json.dumps(requestData)
    url = basicUrl + '/UpdateMachineStatus'
    try:
        response = requests.request("POST", url, headers=headers, data=TransferJSONData, timeout=10)
        #print(response)

        data = response.json()
        #print(data)
        AnaylsisCommand(data)
    except requests.exceptions.RequestException as e:
        print(ANSI_RED + '[Error] ' + str(e) + ANSI_OFF)  

def AnaylsisCommand(response):
    print(ANSI_BLUE + '[Info] Start to anaylsis response from data platform!' + ANSI_OFF)

def CloudType0_GetThresholdValue():
    url = MyParameter.CloudUrl + '/getAntiquitiesWarningValue?token=' + MyParameter.UserToken

    payload={}
    headers={}

    try:
        response = requests.request('GET', url, headers=headers, data=payload)
        getData = response.json()
    
        CloudType0_AnaylsisGetThresholdValue(getData)
    except requests.exceptions.RequestException as e:
        print(ANSI_RED + '[Error] ' + str(e) + ANSI_OFF)

def CloudType0_AnaylsisGetThresholdValue(response):
    try:
        res = response['res']

        if res == 1:
            MyParameter.VibrationWarningValue = response['VibrationWarningValue']
            MyParameter.VibrationAlarmValue = response['VibrationAlarmValue']
            MyParameter.FireWarningTempValue = response['FireWarningTempValue']
            MyParameter.FireWarningCountValue = response['FireWarningCountValue']
            MyParameter.FireAlarmTempValue = response['FireAlarmTempValue']
            MyParameter.FireAlarmCountValue = response['FireAlarmCountValue']
            MyParameter.CapturePictureRH = response['CapturePictureRH']
            MyParameter.CapturePictureRV = response['CapturePictureRV']
            MyParameter.CaptureVideoSecond = response['CaptureVideoSecond']
            MyParameter.SensorsFValue = response['SensorsFValue']
            MyParameter.CameraFValue = response['CameraFValue']
            MyParameter.UpdateFValue = response['UpdateFValue']
        else:
            print(ANSI_RED + '[Error] Transfer Cloud Type 0 Get Function Error!' + ANSI_OFF)
    except:
        print(ANSI_RED + '[Error] Anaylsis Threshold Value happen error!'+ ANSI_OFF)

def CloudType0_UpdateValue():

    global aCloudType0UpdateData

    url = MyParameter.CloudUrl + '/addSensorValue'

    aCloudType0UpdateData['token']=MyParameter.UserToken
    payload = json.dumps(aCloudType0UpdateData)
    #print(payload)
    headers={'Content-Type':'application/json'}
    print(payload)
    print(ANSI_YELLOW + '[Update] Start to update data to cloud!'+ ANSI_OFF)

    try:
        response= requests.request('POST', url, headers=headers, data=payload)

        getData = response.json()

        CloudType0_AnalysisUpdateValue(getData)

    except requests.exceptions.RequestException as e:
        print(ANSI_RED + '[Error] ' + str(e) + ANSI_OFF)

def CloudType0_AnalysisUpdateValue(response):
    #print(response)
    try:
        result = response['res']
    except:
        print(ANSI_RED + '[Error] Anaylsis Update Value happen error!'+ ANSI_OFF)

def DoWork(macaddress):
    global tCheckTimer_Start
    global tCheckTimer_CloudType0_Get
    global tCheckTimer_CloudType0_Update


    global bCloudType0UpdateTrigger

    checkFunctionIntervalTime = time.time() - tCheckTimer_Start
    checkCloudType0_Get_IntervalTime = time.time() - tCheckTimer_CloudType0_Get
    checkCloudType0_Update_IntervalTime = time.time() - tCheckTimer_CloudType0_Update

    if checkFunctionIntervalTime < 0:
        tCheckTimer_Start = time.time()

    if checkCloudType0_Get_IntervalTime < 0:
        tCheckTimer_CloudType0_Get = time.time()
    
    if checkCloudType0_Update_IntervalTime < 0:
        tCheckTimer_CloudType0_Update = time.time()

    if MyParameter.IsDataPlatformConnected and (checkFunctionIntervalTime >= 30):
        tCheckTimer_Start = time.time()
        print(ANSI_BLUE + '[Info] Start to communication data platform!' + ANSI_OFF)
        UpdateMachineStatus(macaddress)

    if MyParameter.UseCloud > 0:
        if MyParameter.CloudType == 0:
            if checkCloudType0_Get_IntervalTime >= 60:
                print(ANSI_BLUE + '[Info] Start to get threshold value from cloud!' + ANSI_OFF)
                tCheckTimer_CloudType0_Get = time.time()
                CloudType0_GetThresholdValue()

            if checkCloudType0_Update_IntervalTime >= 60: #1800:
                if bCloudType0UpdateTrigger==True:
                    bCloudType0UpdateTrigger = False
                    print(ANSI_BLUE + '[Info] Start to update value to cloud!' + ANSI_OFF)
                    tCheckTimer_CloudType0_Update = time.time()
                    CloudType0_UpdateValue()
