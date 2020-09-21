import smbus
import math
import time
import board
import adafruit_dht

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
