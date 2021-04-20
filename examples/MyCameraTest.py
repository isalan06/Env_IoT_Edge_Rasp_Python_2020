# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1600,900)
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array


gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("Light:", gray_image.mean())

# display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)

