# For more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import cv2
import numpy as np
import os
import imutils
import sys
from glob import glob  
import json  
import base64  
from subprocess import Popen, PIPE  
from wand.image import Image

# Playing video from file:
# cap = cv2.VideoCapture('vtest.avi')
# Capturing video from webcam:
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,360)
cap.set(5,8)
currentFrame = 0

# Get current width of frame
width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) # float


# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'X264')

# while(True):
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:
        # Handles the mirroring of the current frame
        #frame = cv2.flip(frame,1)
        #frameResize = imutils.resize(frame, 640)
        sys.stdout.write( frame.tostring() )
        # Saves for video
        #out.write(frame)

        # Display the resulting frame
        #cv2.imshow('frame',frame)
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # To stop duplicate images
    currentFrame += 1

# When everything done, release the capture
cap.release()
#out.release()
#cv2.destroyAllWindows()
    