#!/usr/bin/python3

import os
import picamera
import time
from datetime import datetime
import requests

response = os.system("ping -c 1 192.168.8.100")

nowtime = datetime.now()
datestring = nowtime.strftime('%Y%m%d')
fileString ="Pictures/" + datestring + "/"
if not os.path.isdir("Pictures/"):
    os.mkdir("Pictures/")
if not os.path.isdir(fileString):
    os.mkdir(fileString)
filename = nowtime.strftime('%Y%m%d%H%M%S') + ".jpg"
fileString += filename

with picamera.PiCamera() as camera:
    camera.resolution = (1024,768)
    time.sleep(1.0)
    camera.capture(fileString)

if response == 0:
    setsn=1
    setfilename=filename
    setdatetime=nowtime.strftime('%Y%m%d%H%M%S')
    url = "http://192.168.8.100:5099/Update/JpgPicture?sn=" + setsn + "&filename=" + setfilename + "&datetime=" + setdatetime
    file=open('test','rb')
    payload=file.read()
    file.close()
    headers = {'Content-Type': 'image/jpeg'}
    responses = requests.request("POST", url, headers=headers, data = payload)
    print(responses.text.encode('utf8'))
