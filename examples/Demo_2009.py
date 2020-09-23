import smbus
import math
import time
import board
import adafruit_dht
import json
import requests
import datetime
import ssl

#Vibration Power Management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

#Vibration Attribute
vib_bus = smbus.SMBus(1)
vib_address = 0x68
gyro_xout = 0
gyro_yout = 0
gyro_zout = 0
gyro_xout_scaled = 0
gyro_yout_scaled = 0
gyro_zout_scaled = 0
accel_xout = 0
accel_yout = 0
accel_zout = 0
accel_xout_scaled = 0
accel_yout_scaled = 0
accel_zout_scaled = 0
x_rotation = 0
y_rotation = 0

#Vibration Function
def read_byte(adr):
    return vib_bus.read_byte_data(vib_address, adr)

def read_word(adr):
    high = vib_bus.read_byte_data(vib_address, adr)
    low = vib_bus.read_byte_data(vib_address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if(val > 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)

def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


# DHT22 Attribute
dhtDevice = adafruit_dht.DHT22(board.D17)
temp_c=0.0
humidity=0

#Vibration - Now make the 6050 up as it starts in sleep mode
vib_bus.write_byte_data(vib_address, power_mgmt_1, 0)

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

    #Vibration
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)
    gyro_xout_scaled = gyro_xout / 131
    gyro_yout_scaled = gyro_yout / 131
    gyro_zout_scaled = gyro_zout / 131
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
    x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    y_rotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    print("gyro_xout:" + str(gyro_xout) + "-" + str(gyro_xout_scaled) + ";gyro_yout:" + str(gyro_yout) + "-" + str(gyro_yout_scaled) + ";gyro_zout:" + str(gyro_zout) + "-" + str(gyro_zout_scaled))
    print("accel_xout:" + str(accel_xout) + "-" + str(accel_xout_scaled) + ";accel_yout:" + str(accel_yout) + "-" + str(accel_yout_scaled) + ";accel_zout:" + str(accel_zout) + "-" + str(accel_zout_scaled))
    print("x_rotation:" + str(x_rotation) + ";y_rotation:" + str(y_rotation))

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

    setKey2="Vibration"
    InformationData[SetKey][SetKey2]={}
    InformationData[SetKey][SetKey2]["Count"]=1
    InformationData[SetKey][SetKey2][SetKey3]=[]
    VibrationList={}
    VibrationList["ID"]=1
    VibrationList["Type"]="Gateway"
    VibrationList["GyroUnit"]="DegreePerSecond"
    VibrationList["GyroX"]=gyro_xout
    VibrationList["GyroXScaled"]=gyro_xout_scaled
    VibrationList["GyroY"]=gyro_yout
    VibrationList["GyroYScaled"]=gyro_yout_scaled
    VibrationList["GyroZ"]=gyro_zout
    VibrationList["GyroZScaled"]=gyro_zout_scaled
    VibrationList["AccelUnit"]="g"
    VibrationList["AccelX"]=accel_xout
    VibrationList["AccelXScaled"]=accel_xout_scaled
    VibrationList["AccelY"]=accel_yout
    VibrationList["AccelYScaled"]=accel_yout_scaled
    VibrationList["AccelZ"]=accel_zout
    VibrationList["AccelZScaled"]=accel_zout_scaled
    VibrationList["RotationUnit"]="Degree"
    VibrationList["RotationX"]=x_rotation
    VibrationList["RotationY"]=y_rotation
    InformationData[SetKey][SetKey2][SetKey3].append(VibrationList)

    TransferJSONData=json.dumps(InformationData)
    print(TransferJSONData)

    try:
        auth=('token', 'example')
        ssl._create_default_https_context = ssl._create_unverified_context
        headers = {'Content-Type': 'application/json'}
        r = requests.post('https://script.google.com/macros/s/AKfycbwOx-ypSoziN9f9__rit-_J3bjYP8sSOPoIfzo1rqi3QRIl-DQ/exec',headers=headers, data=TransferJSONData, auth=auth)
        print(r)
    except BaseException as error:
        print(error)




