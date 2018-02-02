from time import gmtime, strftime
import RPi.GPIO as GPIO ## Import GPIO library
import time
import datetime
import imutils
import numpy as np
import cv2
import argparse
import os
from subprocess import Popen, PIPE  
import ConfigParser

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

if os.path.exists("/home/pi/usb/config.ini") == False:
    print("config.ini error")
    os.system('sudo mount /dev/sda1 /home/pi/usb')
    exit()
    
Config = ConfigParser.ConfigParser()
Config.read('/home/pi/usb/config.ini')

id =  ConfigSectionMap('Profile')['id']
timevdo = ConfigSectionMap('Profile')['timevdo']
timepic = ConfigSectionMap('Profile')['timepic']
key0 = ConfigSectionMap('Profile')['key0']
key1 = ConfigSectionMap('Profile')['key1']
rest = ConfigSectionMap('Profile')['rest']


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="/home/pi/usb/",
	help="path to output")
ap.add_argument("-i", "--idcamera", type=int, default=0,
	help="camera should be used")
ap.add_argument("-f", "--firmrate", type=int, default=10,
	help="frame rate")
ap.add_argument("-c", "--timepic", type=float, default=0.9,# 0.95
	help="save pic evev sec(sec)")
args = vars(ap.parse_args())


ffmpeg_call = ("ffmpeg -f v4l2 -r 10 -s ")
ffmpeg_call += rest
ffmpeg_call += (" -i /dev/video")
ffmpeg_call += str(args["idcamera"])
ffmpeg_call += (" -f s16le -ac 2 -i /dev/zero"
              " -c:v libx264 -pix_fmt yuv420p -preset ultrafast -g 20 -b:v 820k -c:a aac -ar 44100 -threads 0 -bufsize 512k"
              " -f flv rtmp://a.rtmp.youtube.com/live2/")
if args["idcamera"] == 0:
    ffmpeg_call += key0
else:
    ffmpeg_call += key1


print ffmpeg_call
ffmpeg_call = ffmpeg_call.split(" ")
print ffmpeg_call



print("Camera "+str(args["idcamera"])) 

proc = Popen(ffmpeg_call)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(4, GPIO.IN) # Power
GPIO.setup(17,GPIO.OUT)

while(GPIO.input(4) == 0):
    print("Ok!!!")
    time.sleep(0.2)
    GPIO.output(17,True)
    time.sleep(0.2)
    GPIO.output(17,False)

while(True):
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #print ffmpeg_call
    if(GPIO.input(4) == 0):
        break
    

print("Ok!!!") 
GPIO.cleanup()
proc.kill()  