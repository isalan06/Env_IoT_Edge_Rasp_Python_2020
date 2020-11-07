#!/usr/bin/python3

import os
import picamera
import time
from datetime import datetime


nowtime = datetime.now()
datestring = nowtime.strftime('%Y%m%d')
fileString ="Pictures/" + datestring + "/"
if not os.path.isdir("Pictures/"):
    os.mkdir("Pictures/")
if not os.path.isdir(fileString):
    os.mkdir(fileString)
fileString += datetime.now().strftime('%Y-%m-%d %H:%M:%S')
fileString += ".jpg"

with picamera.PiCamera() as camera:
    camera.resolution = (1024,768)
    time.sleep(1.0)
    camera.capture(fileString)