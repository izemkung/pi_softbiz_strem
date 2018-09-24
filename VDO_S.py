from time import gmtime, strftime
import RPi.GPIO as GPIO ## Import GPIO library
import time
import datetime
import imutils
import numpy as np
import cv2
import argparse
import os
import subprocess as sp 
import ConfigParser
import socket

REMOTE_SERVER = "www.google.com"


def internet_on():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False
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

strem_address0	= ConfigSectionMap('Profile')['strem_address0']
strem_port0	= ConfigSectionMap('Profile')['strem_port0']
strem_application0 = ConfigSectionMap('Profile')['strem_application0']
strem_name0	= ConfigSectionMap('Profile')['strem_name0']
strem_address1	= ConfigSectionMap('Profile')['strem_address1']
strem_port1	= ConfigSectionMap('Profile')['strem_port1']
strem_application1 = ConfigSectionMap('Profile')['strem_application1']
strem_name1	= ConfigSectionMap('Profile')['strem_name1']


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
              " -f flv rtmp://")
if args["idcamera"] == 0:
    ffmpeg_call += strem_address0
    ffmpeg_call += (":")
    ffmpeg_call += strem_port0
    ffmpeg_call += ("/")
    ffmpeg_call += strem_application0
    ffmpeg_call += ("/")
    ffmpeg_call += strem_name0
else:
    ffmpeg_call += strem_address1
    ffmpeg_call += (":")
    ffmpeg_call += strem_port1
    ffmpeg_call += ("/")
    ffmpeg_call += strem_application1
    ffmpeg_call += ("/")
    ffmpeg_call += strem_name1


print ffmpeg_call
ffmpeg_call = ffmpeg_call.split(" ")
print ffmpeg_call



print("Camera "+str(args["idcamera"])) 



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

if internet_on() == True :
    proc = sp.Popen(ffmpeg_call, stdout=sp.PIPE)
else:
    GPIO.cleanup()
    exit()

print("Loop") 
while(True):
    GPIO.output(17,True)
    time.sleep(2)
    rc = proc.poll()
    print("Process Return coder>>"+str(rc)+"<<") 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        proc.kill()
        break
    #print ffmpeg_call
    if(GPIO.input(4) == 0):
        proc.kill()
        break
    if proc.poll() != None : 
        break
    if internet_on() != True : 
        proc.kill()
        break

print("Ok!!! End ") 
GPIO.cleanup()
#proc.kill()  