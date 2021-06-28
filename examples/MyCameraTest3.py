#https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
#https://www.pyimagesearch.com/2016/02/22/writing-to-video-with-opencv/
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime
import cv2
from imutils.video import VideoStream

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1920, 1088)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1920, 1088))

#Define the codec
today = time.strftime("%Y%m%d-%H%M%S")
fps_out = 32
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(today + ".avi", fourcc, fps_out, (1920, 1088))

# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    #save the frame to a file
    out.write(image)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break