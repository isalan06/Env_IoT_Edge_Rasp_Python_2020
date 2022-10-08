from pathlib import Path
import MyParameter

import json
import requests
import os
import ssl

basicUrl='http://211.75.141.1:40080/Gateway'
_macaddress=''

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

def getMachineInformation(macaddress):

    global _macaddress
    global basicUrl

    _macaddress = macaddress

    print(ANSI_WHITE + '[Info] Start to get machine information from data platform!' + ANSI_OFF)

    requestData={}
    requestData['MacAddress']=_macaddress

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
            MyParameter.IsDataPlatformConnected=True
            MyParameter.Token = data['Token']
            MyParameter.UseCloud = False if (data['UseCloud'] == 0) else True
            MyParameter.UserToken = data['UserToken']
            MyParameter.CloudUrl = data['CloudUrl']
            MyParameter.CloudType = data['CloudType']
        elif result == 3:
            url = basicUrl + '/AddMacAddress'
            requestData['Location']=''
            requestData['UseCloud']=0
            requestData['CloudUrl']=''
            requestData['CloudType']=0
            requestData['UserToken']=''
            requestData['Longitude']=0
            requestData['Latitude']=0
            TransferJSONData2=json.dumps(requestData)
            response2 = requests.request("POST", url, headers=headers, data=TransferJSONData2, timeout=10)
            data = response2.json()
            if result==0:
                MyParameter.IsDataPlatformConnected=True
                MyParameter.Token = data['Token']


        print(ANSI_WHITE + '[Info] Finish getting machine information from data platform!' + ANSI_OFF)
        if MyParameter.IsDataPlatformConnected:
            print(ANSI_WHITE + '[Info] Start to update data to data platform!' + ANSI_OFF)
        else:
            print(ANSI_RED + '[Error] Cannot update data to data platform' + ANSI_OFF)

                        
    except requests.exceptions.RequestException as e:
        print(ANSI_RED + '[Error] ' + str(e) + ANSI_OFF)