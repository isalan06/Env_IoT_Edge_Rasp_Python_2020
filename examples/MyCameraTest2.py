# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

print('Input Width: ')
width=int(input())
print('Input Height: ')
height=int(input())
print('Input Shutter Speed: ')
shutter_speed = int(input())
print('Input Rotation')
rotation = int(input())

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution=(width, height)
camera.shutter_speed=shutter_speed
camera.rotation=rotation
rawCapture = PiRGBArray(camera, size=(width, height))
# allow the camera to warmup
time.sleep(0.1)
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
# display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)