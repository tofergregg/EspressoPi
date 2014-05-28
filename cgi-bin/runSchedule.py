#!/usr/bin/env python

import datetime
import time
import subprocess
import sys

days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def powerOn(pin):
	output = subprocess.check_output(["/home/pi/www/cgi-bin/CheckOnLED.py",str(pin)])
	if "On" in output:
		return "On"
	elif "Off" in output:
		return "Off"
	elif "Blinking" in output:
		return "Blinking"

while (1):
	todayComplete = False
	today = datetime.datetime.today()

	dayOfWeek = days[today.weekday()]

	schedule = []
	with open("times.txt","r") as f:
		for line in f:
			line = line[:-1]
			schedule.append(line.split(','))

	for day in schedule:
		if day[4] == 'false':
			continue
		#print day
		day[1] = int(day[1])
		if day[3]=='PM':
			if day[1]!=12:
				day[1]=day[1]+12
		else:
			if day[1]==12:
				day[1]=0
		if day[0]==dayOfWeek:
			if day[1]==today.hour:
				if int(day[2])==today.minute:
					print "Turning on:",today.hour,today.minute
					# first, check if it is on already
					onLED_status = powerOn(4)
					print "ON status is: ",onLED_status
					if onLED_status != "On": # turn it on
						print subprocess.check_output(["/home/pi/www/cgi-bin/TurnOnVivaldi.py"])
						# now check the steam LED
						steamLED_status = powerOn(17)
						print "Steam is: ",steamLED_status
						if day[5]=="(Steam)": # we want steam
							if steamLED_status == "Off":
								print subprocess.check_output(["/home/pi/www/cgi-bin/TurnOnSteamButton.py"])
								print "Turning on Steam"
						else: # no steam
							if steamLED_status != "Off":
								print subprocess.check_output(["/home/pi/www/cgi-bin/TurnOffSteamButton.py"])
								print "Turning off Steam"
					time.sleep(120) # sleep until we're past today's scheduled time to start
	print str(today).split('.')[:-1][0]
	sys.stdout.flush()
	time.sleep(5)
	


