#!/usr/bin/python

import sys
import subprocess
import json
import cgi
import cgitb
cgitb.enable()

sys.stdout.write("Content-Type: json/text")
sys.stdout.write("\r\n")
sys.stdout.write("\r\n")

form = cgi.FieldStorage()

times=[]
try:
	with open("times.txt","r") as f:
		for line in f:
			times.append(line.split(','))
			times[-1][-1]=times[-1][-1][:-1]
		print json.dumps(times)
except:
	print json.dumps("")
