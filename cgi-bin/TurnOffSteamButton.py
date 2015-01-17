#!/usr/bin/python

import sys
import subprocess
import time
import cgitb
cgitb.enable()

# sudo adduser www-data gpio

sys.stdout.write("Content-Type: text/html")
sys.stdout.write("\r\n")
sys.stdout.write("\r\n")

subprocess.check_output(["/usr/local/bin/gpio-admin", "export", "22"])

with open("/sys/devices/virtual/gpio/gpio22/direction","w") as f:
	f.write("out\n");
	
with open("/sys/devices/virtual/gpio/gpio22/value","w") as f:
	f.write("1\n"); # turn on pin

time.sleep(4);

with open("/sys/devices/virtual/gpio/gpio22/value","w") as f:
	f.write("0\n"); # turn off pin

subprocess.check_output(["/usr/local/bin/gpio-admin", "unexport", "22"])

print "Turned off Steam Boiler"
