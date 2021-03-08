#!/usr/bin/python3
#MyCamera.py

import os
import cv2
import picamera

bCameraUsed = False


def CreateImageFileName(folderString):
    if not os.path.isdir("/home/pi/Pictures/Pictures/"):
        os.mkdir("/home/pi/Pictures/Pictures/")
    if not os.path.isdir(folderString):
        os.mkdir(folderString)
    filename = "sn_" + nowtime.strftime('%Y-%m-%d %H-%M-%S') + ".jpg"
    return filename