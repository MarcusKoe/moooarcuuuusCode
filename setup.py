#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import apt
import sys
from time import sleep as sleep
import time
import subprocess
from ConfigParser import SafeConfigParser
from pythonfunctions import rm
from pythonfunctions import mkdir
from pythonfunctions import find
from pythonfunctions import rmdir

cron_selectbutton = '@reboot /usr/bin/nice -n 19 /usr/bin/ionice -c3 /usr/bin/ionice -c 3 /usr/bin/python /home/pi/moooarcuuuusCode/execute-selectbutton-controllerflashing.py >> /home/pi/moooarcuuuusCode/execute-selectbutton-controllerflashing.py.logfile.txt 2>&1'
cron_ports = '@reboot /usr/bin/nice -n 19 /usr/bin/ionice -c3 /usr/bin/ionice -c 3 /usr/bin/python /home/pi/moooarcuuuusCode/execute-ports-controllerflashing.py >> /home/pi/moooarcuuuusCode/execute-ports-controllerflashing.py.logfile.txt 2>&1'

d_usr = '/home/pi'
d_bse = os.path.join(d_usr, 'moooarcuuuusCode')

currentdir = os.getcwd()

if (not currentdir == d_bse):
	print('Wrong directory')
	sys.exit()

warning = '\n \nParts of this program are not created by me. These parts can have their own licenses. The following license text only refers to my program code.\n \n This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3. \n \n This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. \n \n You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>. \n \n THIS IS UNSTABLE SOFTWARE! \n \n THIS SOFTWARE WORKS ONLY WITH KITES SAIO BOARD!!! \n \n'

print(warning)

yesno = raw_input('Accept? Type "YES" or "NO"  ')
if (not yesno == 'YES'):
	print("Have a nice day")
	sys.exit()

sleep(1)
print('Generate list of installed packages, this can take a while')
packagecache = apt.Cache()






def makeconfig():
	print('Configuration...')
	print('What board do you have? \n')
	bvers = raw_input('Type "0.5" or "0.6" ')
	if not (bvers == '0.5' or bvers == '0.6'):
		print('No valid input')
		sys.exit()
	print('What screen do you have? \n')
	screensize = raw_input('Type "320x240" or "640x480" ')
	if not (screensize == '320x240' or screensize == '640x480'):
		print('No valid input')
		sys.exit()
	xres = screensize[0:3]
	yres = screensize[4:7]
	#print(xres)
	#print(yres)
	parser = SafeConfigParser()
	parser.add_section('general')
	parser.set('general', 'boardversion', bvers)
	parser.set('general', 'xres', xres)
	parser.set('general', 'yres', yres)
	with open(f_conf, 'w') as cfile:
		parser.write(cfile)
	return(bvers)

f_conf = os.path.join(d_bse, 'configuration.ini')
bvers = makeconfig()


print('Should the "crontab" (autostart) be updated?')
yesno = raw_input('Type "YES" or "NO" ')
if (yesno == 'NO'):
	None
elif (yesno == 'YES'):
	result = subprocess.check_output('crontab -l', shell=True)
	print('Would you add the "selectbutton" method (buttons on RPI GPIO 24 and 25)?')
	yesno = raw_input('Type "YES" or "NO"  ')
	if (yesno == 'YES'):
		if ('execute-selectbutton-controllerflashing.py' in result):
			print('Selectbutton already exists, skip insert')
		else:
			os.system('(crontab -l 2>/dev/null; echo "\n \n' + cron_selectbutton + '")| crontab -')
		
		if not packagecache['avrdude'].is_installed or not packagecache['imagemagick'].is_installed:
			print('You need "avrdude" and "imagemagick" installed')
			print('Should I execute:')
			aptstring = "sudo apt-get update && sudo apt-get install -y avrdude imagemagick"
			print(aptstring)
			yesno = raw_input('Type "YES" or "NO" ')
			if (yesno == 'YES'):
				os.system(aptstring)
				print('Generate list of installed packages, this can take a while')
				packagecache = apt.Cache()
		print('Make pngview executable')
		b_pngv = os.path.join(d_bse, 'pngview')
		chmodcommand = 'chmod +x ' + b_pngv
		os.system(chmodcommand)

	print('\n\nWould you add the "ports" method (select with ports in ES)?')
	yesno = raw_input('Type "YES" or "NO"  ')
	if (yesno == 'YES'):
		if ('execute-ports-controllerflashing.py' in result):
			print('Ports already exists, skip insert')
		else:
			os.system('(crontab -l 2>/dev/null; echo "\n \n' + cron_ports + ' \n")| crontab -')	
		
		if not (packagecache['avrdude'].is_installed):
			print('You need "avrdude" installed')
			print('Should I execute:')
			aptstring = "sudo apt-get update && sudo apt-get -y install avrdude"
			print(aptstring)
			yesno = raw_input('Type "YES" or "NO" ')
			if (yesno == 'YES'):
				os.system(aptstring)
else:
	print('No valid input')
	sys.exit()





	
sleep(1)

print('If you are using this program for the first time, you should install the keyboardmouse layout and restart the system. You must then reconfigure the input device. On the "Configure Input" screen hold down R1 in the input window and press X or Y.')

print('\nWould you install the keyboardmouse layout and restart the system?')
yesno = raw_input('Type "YES" or "NO"  ')
if (yesno == 'YES'):
	flashcommand = 'sh flash.sh arduino-precompiled-ports/' + bvers + '/SAIO_v2a-MouseKeyboard.ino.hex'
	os.system(flashcommand)
	sleep(1)
	rebootcommand = 'sudo reboot'
	os.system(rebootcommand)
else:
	print('Installation done \n \n Have a nice day')
