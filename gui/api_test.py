#!flask/bin/python
from flask import Flask
from flask import request
import os
import base64
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/qrcode', methods=['POST'])
def qrcode():
    print('get qrcode' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
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
    if os.path.exists(triggerfilename):
        os.remove(triggerfilename)
    infofilename = '/home/pi/Data/info.txt'
    if os.path.exists(infofilename):
        os.remove(infofilename)
    imagefilename = '/home/pi/Data/person.jpg'
    if os.path.exists(imagefilename):
        os.remove(imagefilename)

    f = open(infofilename, 'w')
    f.write(qrcode + '\n')
    #f.write(str(temperature) + '\n')
    f.write(format(temperature, '.1f') + '\n')
    f.write(createtime + '\n')
    f.write(sensortype)
    f.close()
    print('Write Information File')

    img_str = data['imageData']
    img_data = base64.b64decode(img_str)
    with open(imagefilename, 'wb') as f2:
        f2.write(img_data)
        print('Write Image File')
        

    with open(triggerfilename, 'w') as f3:
        f3.write('Trigger')
        print('Write Trigger File - ' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))


    return "OK"


if __name__ == '__main__':
    apiserverfilename = '/home/pi/Data/apiserver.txt'
    if os.path.exists(apiserverfilename) == False:
        with open(apiserverfilename, 'w') as f4:
            f4.write('API Server')
    app.run(host='192.168.2.100', debug=True)
    print("Test")
    if os.path.exists(apiserverfilename):
        os.remove(apiserverfilename)