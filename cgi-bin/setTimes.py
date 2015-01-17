#!/usr/bin/python

import sys
import os
import subprocess
import cgi
import cgitb
import json
cgitb.enable()

sys.stdout.write("Content-Type: text/html")
sys.stdout.write("\r\n")
sys.stdout.write("\r\n")

form = cgi.FieldStorage()

open("times.lck","a").close()
with open("times.txt","w") as f:
	times = json.loads(form['times'].value)
	print times
	for day in times:
		f.write(day+"\n")

os.remove("times.lck")