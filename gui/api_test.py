#!flask/bin/python
from flask import Flask
from flask import request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/qrcode', methods=['POST'])
def qrcode():
    print('get qrcode')
    qrcode = None
    data = request.get_json()
    if data and "qrcode" in data:
        qrcode = data["qrcode"]
    temperature = data["temperature"]
    createtime = data['createDate']
    sensortype = data['type']
    print('ID:' + qrcode)
    print('Temperature:' + str(temperature))

    triggerfilename = '/home/pi/Data/trigger.txt'
    if path.exists(triggerfilename):
        os.remove(triggerfilename)
    infofilename = '/home/pi/Data/info.txt'
    if path.exists(infofilename):
        os.remove(infofilename)
    imagefilename = '/home/pi/Data/person.jpg'
    if path.exists(imagefilename):
        os.remove(imagefilename)

    f = open(infofilename, 'w')
    f.write(qrcode)
    f.write(temperature)
    f.write(createtime)
    f.write(sensortype)
    f.close()


    return "OK"


if __name__ == '__main__':
    app.run(host='192.168.1.163', debug=True)
    print("Test")