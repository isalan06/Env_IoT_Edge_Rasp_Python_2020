import smbus
import math
import time
import board
import adafruit_dht
import json
import requests
import datetime
import ssl

# DHT22 Attribute
dhtDevice = adafruit_dht.DHT22(board.D17)
temp_c=0.0
humidity=0

while True:
    time.sleep(10.0)

    #DHT22
    try:
        temp_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print("Temp: {:.1f}C Humidity: {}%".format(temp_c, humidity))
    except RuntimeError as error:
        print(error.args[0])
        continue

    #JSON
    SetKey="Machine"
    SetValue="IoT Edge"
    InformationData = {}
    InformationData[SetKey]=SetValue
    InformationData["Machine ID"]="Test ID"
    InformationData["Comm Type"]="4G"
    InformationData["Gateway Time"]=datetime.datetime.now().strftime("%Y%m%d%H%M%S")	
    SetKey="Data"
    InformationData[SetKey]={}
    SetKey2="Temp"
    SetKey3="Data"
    InformationData[SetKey][SetKey2]={}
    InformationData[SetKey][SetKey2]["Count"]=1
    InformationData[SetKey][SetKey2][SetKey3]=[]
    templist = {}
    templist["ID"]=1
    templist["Type"]="Gateway"
    templist["Unit"]="C"
    templist["Value"]=temp_c
    InformationData[SetKey][SetKey2][SetKey3].append(templist)
    
    SetKey2="Humidity"
    InformationData[SetKey][SetKey2]={}
    InformationData[SetKey][SetKey2]["Count"]=1
    InformationData[SetKey][SetKey2][SetKey3]=[]
    humiditylist = {}
    humiditylist["ID"]=1
    humiditylist["Type"]="Gateway"
    humiditylist["Unit"]="%RH"
    humiditylist["Value"]=humidity
    InformationData[SetKey][SetKey2][SetKey3].append(humiditylist)

    TransferJSONData=json.dumps(InformationData)
    print(TransferJSONData)

    auth=('token', 'example')

    
    ssl._create_default_https_context = ssl._create_unverified_context
    headers = {'Content-Type': 'application/json'}
    r = requests.post('https://script.google.com/macros/s/AKfycbwOx-ypSoziN9f9__rit-_J3bjYP8sSOPoIfzo1rqi3QRIl-DQ/exec',headers=headers, data=TransferJSONData, auth=auth)
    print(r)




