#!/usr/bin/env python

import sys
import subprocess
import time
import cgi
import cgitb
cgitb.enable()

# sudo adduser www-data gpio

sys.stdout.write("Content-Type: text/html")
sys.stdout.write("\r\n")
sys.stdout.write("\r\n")

# the first argument is the pin number
# pin 4 = ON LED
# pin 17 = STEAM LED
try:
	form = cgi.FieldStorage()
	pin = form["LED_num"].value
except KeyError:
	pin = sys.argv[1]

# set the pin as an export pin
try:
	subprocess.check_output(["gpio-admin", "export", pin,"pulldown"])
except subprocess.CalledProcessError, e:
	pass # might already be set as export pin

# the LED will either be off or blinking, and the rate is approximately 1Hz
# So, we check for two seconds at a rate of 0.1Hz, and count the number
# of ons and offs
onCount = 0
offCount = 0

checkCount = 0
totalCount = 0
while checkCount < 20:
	totalCount += 1
	if totalCount == 100:
		# can't seem to check
		print "Cannot check now"
		quit()
	try:
		with open("/sys/devices/virtual/gpio/gpio"+pin+"/value","r") as f:
			pinValue = f.readline()[:-1]
			print pinValue
			if pinValue=="1": onCount+=1
			if pinValue=="0": offCount+=1	
		checkCount += 1
	except IOError:
		# permission denied? try again
		print "can't check...retrying"
	time.sleep(0.1);

subprocess.check_output(["gpio-admin", "unexport", pin])

print "pin:",pin
print "onCount:",onCount
print "offCount:",offCount
if onCount > 0 and offCount > 0: # either blinking or ON
	if onCount < 13:
		print "Blinking"
	else:
		print "On"

elif onCount == 0: # if there aren't any ONs, then it is OFF
	print "Off"


