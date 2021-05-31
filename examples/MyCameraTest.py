# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

import base64
from PIL import Image
from io import BytesIO

def frame2base64(frame):
    img = Image.fromarray(frame) #將每一幀轉為Image
    output_buffer = BytesIO() #建立一個BytesIO
    img.save(output_buffer, format='JPEG') #寫入output_buffer
    byte_data = output_buffer.getvalue() #在記憶體中讀取
    sSmallImageData = base64.b64encode(byte_data) #轉為BASE64
    print(sSmallImageData)

# initialize the camera and grab a reference to the raw camera capture
print("Start")
camera = PiCamera()
camera.resolution = (640,480)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# grab an image from the camera
print("Capture")
rawCapture.truncate(0)
camera.capture(rawCapture, format="bgr")
print("Transfer")
image = rawCapture.array


gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("Light:", gray_image.mean())
frame2base64(rawCapture)

# display the image on screen and wait for a keypress
cv2.imshow("Image", image)
#cv2.waitKey(0)

