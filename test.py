from glob import glob  
import json  
import base64  
import os  
from subprocess import Popen, PIPE  
import argparse
from time import gmtime, strftime
import RPi.GPIO as GPIO ## Import GPIO library
import time
import datetime
import imutils
import numpy as np
import cv2
import ConfigParser

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 10)
cap.set(3,640)
cap.set(4,360)
#cap.set(5,20)

ffmpeg_call = ("ffmpeg -threads 4 -r 20 -f image2pipe -s 640x360 -vcodec mjpeg"  
               " -i -"
               " -f s16le -ac 2 -i /dev/zero"
               " -f flv rtmp://a.rtmp.youtube.com/live2/99d3-k6t5-b7t0-ddq0")
ffmpeg_call = ffmpeg_call.split(" ")
print ffmpeg_call 
proc = Popen(ffmpeg_call, stdin=PIPE, bufsize=0)


font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.putText(frame,"Car {}".format(strftime("%d %b %Y %H:%M:%S")) ,(2,(360) - 5), font, 0.3,(0,255,255),1) 
    ret0, buffer0 = cv2.imencode('.jpg', frame)
    proc.stdin.write(buffer0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

proc.stdin.close()  
