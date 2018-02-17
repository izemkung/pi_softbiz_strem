cd /
cd home/pi/3g
sudo /home/pi/3g/umtskeeper --sakisoperators "USBINTERFACE='3' OTHER='USBMODEM' USBMODEM='05c6:9003' APN="CUSTOM_APN" CUSTOM_APN="AIS" APN_USER='internet' APN_PASS='internet'" --sakisswitches "--sudo --console" --devicename 'U20' --log --nat 'no' --httpserver
cd /

