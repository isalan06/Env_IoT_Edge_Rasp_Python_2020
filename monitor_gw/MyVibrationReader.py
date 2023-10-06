#!/usr/bin/python3
#MyVibrationReader.py

import smbus
import math
import MyPrint
from datetime import datetime

class VibrationDataDto:
    #Vibration Attribute
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
    vibrationDataList = {}
    vibrationDataList['LastRecordTime'] = 'NA'
    vibrationDataList['Data'] = [] 

    bRecordVibration = False

    sAccelGaugeStatus = "Stop"

    
    def __init__(self):
        pass

VibrationData = VibrationDataDto()

class VibrationReader:

    #Vibration Attribute
    vib_bus = smbus.SMBus(1)
    vib_address = 0x68

    #Vibration Power Management registers
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c


    def __init__(self):
        pass

    def Start(self):
        global vib_bus
        global vib_address
        global power_mgmt_1
        global power_mgmt_2
        #Vibration - Now make the 6050 up as it starts in sleep mode
        try:
            vib_bus.write_byte_data(vib_address, power_mgmt_1, 0)
            MyPrint.Print_Green("[Vibration Info]Start Vibration Sensor Success")
        except Exception as e:
            MyPrint.Print_Red("[Vibration Info]Start Vibration Sensor Fail")
            print(e)

    def Read(self):
        global VibrationData

        try:
            VibrationData.gyro_xout = self.read_word_2c(0x43)
            VibrationData.gyro_yout = self.read_word_2c(0x45)
            VibrationData.gyro_zout = self.read_word_2c(0x47)
            VibrationData.gyro_xout_scaled = VibrationData.gyro_xout / 131
            VibrationData.gyro_yout_scaled = VibrationData.gyro_yout / 131
            VibrationData.gyro_zout_scaled = VibrationData.gyro_zout / 131
            VibrationData.accel_xout = self.read_word_2c(0x3b)
            VibrationData.accel_yout = self.read_word_2c(0x3d)
            VibrationData.accel_zout = self.read_word_2c(0x3f)
            VibrationData.accel_xout_scaled = VibrationData.accel_xout / 16384.0
            VibrationData.accel_yout_scaled = VibrationData.accel_yout / 16384.0
            VibrationData.accel_zout_scaled = VibrationData.accel_zout / 16384.0
            VibrationData.x_rotation = self.get_x_rotation(VibrationData.accel_xout_scaled, VibrationData.accel_yout_scaled, VibrationData.accel_zout_scaled)
            VibrationData.y_rotation = self.get_y_rotation(VibrationData.accel_xout_scaled, VibrationData.accel_yout_scaled, VibrationData.accel_zout_scaled)


            datalist = {}
            datalist['Gx']=VibrationData.gyro_xout_scaled
            datalist['Gy']=VibrationData.gyro_yout_scaled
            datalist['Gz']=VibrationData.gyro_zout_scaled
            datalist['Ax']=VibrationData.accel_xout_scaled
            datalist['Ay']=VibrationData.accel_yout_scaled
            datalist['Az']=VibrationData.accel_zout_scaled

            try:
                VibrationData.vibrationDataList['Data'].append(datalist)
                VibrationData.vibrationDataList['LastRecordTime']=datetime.now().strftime("%Y%m%d%H%M%S")	
                if len(VibrationData.vibrationDataList['Data']) > 200:
                    del VibrationData.vibrationDataList['Data'][0]
            except Exception as e:
                MyPrint.Print_Red("[Vibration Info]Record Vibration History Failure")


            VibrationData.sAccelGaugeStatus = "Running"
        except BaseException as error:
            MyPrint.Print_Red("[Vibration Info]Get G Sensor Failure")

    #Vibration Function
    #region Vibration Function
    def read_byte(self, adr):
        return vib_bus.read_byte_data(vib_address, adr)

    def read_word(self, adr):
        high = vib_bus.read_byte_data(vib_address, adr)
        low = vib_bus.read_byte_data(vib_address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if(val > 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    #endregion



    