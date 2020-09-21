import smbus
import math
import time
import board
import adafruit_dht
import json

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
    SetKey="Data"
    InformationData[SetKey]={}
    SetKey2="Temp"
    SetKey3="Data"
    InformationData[SetKey][SetKey2]={}
    InformationData[SetKey][SetKey2]["Count"]=1
    InformationData[SetKey][SetKey2][SetKey3]={}
    InformationData[SetKey][SetKey2][SetKey3]["ID"]=1
    InformationData[SetKey][SetKey2][SetKey3]["Type"]="Gateway"
    InformationData[SetKey][SetKey2][SetKey3]["Unit"]="C"
    InformationData[SetKey][SetKey2][SetKey3]["Value"]=temp_c
    SetKey2="Humidity"
    InformationData[SetKey][SetKey2]={}
    InformationData[SetKey][SetKey2]["Count"]=1
    InformationData[SetKey][SetKey2][SetKey3]={}
    InformationData[SetKey][SetKey2][SetKey3]["ID"]=1
    InformationData[SetKey][SetKey2][SetKey3]["Type"]="Gateway"
    InformationData[SetKey][SetKey2][SetKey3]["Unit"]="%RH"
    InformationData[SetKey][SetKey2][SetKey3]["Value"]=humidity

    TransferJSONData=json.dumps(InformationData)
    print(TransferJSONData)





