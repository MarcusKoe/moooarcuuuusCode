#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import apt
import sys
from time import sleep as sleep
import time
import subprocess
from ConfigParser import SafeConfigParser
from pythonfunctions import rm as rm
from pythonfunctions import mkdir as mkdir
from pythonfunctions import find as find
from pythonfunctions import rmdir as rmdir
from pythonfunctions import mv as mv
from pythonfunctions import getVars as getVars
from pythonfunctions import arduinocompile as arduinocompile

#sleep(1000)

cron_selectbutton = '@reboot /bin/sleep 20 && /usr/bin/nice -n 19 /usr/bin/ionice -c3 /usr/bin/python /home/pi/moooarcuuuusCode/execute-selectbutton-controllerflashing.py >> /home/pi/moooarcuuuusCode/execute-selectbutton-controllerflashing.py.logfile.txt 2>&1'
cron_ports = '@reboot /usr/bin/nice -n 19 /usr/bin/ionice -c3 /usr/bin/python /home/pi/moooarcuuuusCode/execute-ports-controllerflashing.py >> /home/pi/moooarcuuuusCode/execute-ports-controllerflashing.py.logfile.txt 2>&1'
cron_arduinocompile = '@reboot /bin/sleep 20 && /usr/bin/nice -n 19 /usr/bin/ionice -c3 /usr/bin/python /home/pi/moooarcuuuusCode/execute-arduinocompile.py >> /home/pi/moooarcuuuusCode/execute-arduinocompile.py.logfile.txt 2>&1'

d_usr = getVars('d_usr')
d_bse = getVars('d_bse')
f_arduinotar = getVars('f_arduinotar')
d_ardupath = getVars('d_ardupath')
d_ardulibaries = getVars('d_ardulibaries')
f_arduexec = getVars('f_arduexec')
f_nicoshid = getVars('f_nicoshid')
d_precsb = getVars('d_precsb')
httpArduino = getVars('httpArduino')
httpNicosHID = getVars('httpNicosHID')

currentdir = os.getcwd()

if (not currentdir == d_bse):
	print('Wrong directory')
	print("Have a nice day")
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



yesno = raw_input('This program requires the arduino framework 1.8.5, if you dont want to download it yet, save it as ' + f_arduinotar +'. Otherwise it will be downloaded now from: ' + httpArduino + '. \n \n Are you ready? \n Type "YES" or "NO"')
if (not yesno == 'YES'):
	print("Have a nice day")
	sys.exit()

if not os.path.isfile(f_arduinotar):
	wgetcmd = 'wget -c ' + httpArduino + ' -O ' + f_arduinotar
	os.system(wgetcmd)

print("Testing for existing arduino, delete if exist")
if os.path.isdir(d_ardupath):
	#print("Delete")
	rmdir(d_ardupath)

print("Extract arduino")
tarext = 'tar xf ' + f_arduinotar
os.system(tarext)

print("Testing arduino, compiling Blink")
arduinotest = 'mkdir -p /dev/shm/ardutest && ./arduino-1.8.5/arduino --verify --board arduino:avr:leonardo --pref build.path=/dev/shm/ardutest arduino-1.8.5/examples/01.Basics/Blink/Blink.ino'
p=(subprocess.call(arduinotest, shell=True, stderr=subprocess.PIPE))
#print(p, "Result")
if (p == 0):
	print("Test of the arduino framework passed")
else:
	#print("Shitload of fail")
	print("Compilation of blink failed")
	print(":( That is very sad")
	print("Have a nice day")
	sys.exit()

sleep(1)

yesno = raw_input('This program requires Nicos HID 2.4.4, if you dont want to download it yet, save it as ' + f_nicoshid +'. Otherwise it will be downloaded now from: ' + httpNicosHID + '. \n \n Are you ready? \n Type "YES" or "NO"')
if (not yesno == 'YES'):
	print("Have a nice day")
	sys.exit()

if not os.path.isfile(f_nicoshid):
	wgetcmd = 'wget -c ' + httpNicosHID + ' -O ' + f_nicoshid
	os.system(wgetcmd)


if not os.path.isfile(f_nicoshid):
	print("Nicos HUD tar not found")
	print("Have a nice day")
	sys.exit()

print("Extract Nicos HID")
tarext = 'tar xf ' + f_nicoshid + ' -C ' + d_ardulibaries
#print(tarext)
os.system(tarext)






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
	return(bvers, xres, yres)

f_conf = os.path.join(d_bse, 'configuration.ini')
bvers, xres, yres = makeconfig()


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

	print('\n\nWould you add the "arduino-autocompile" method (compile new sketches at reboot)?')
	yesno = raw_input('Type "YES" or "NO"  ')
	if (yesno == 'YES'):
		if ('execute-arduinocompile.py' in result):
			print('Arduino-autocompile already exists, skip insert')
		else:
			os.system('(crontab -l 2>/dev/null; echo "\n \n' + cron_arduinocompile + ' \n")| crontab -')
				
				
				
else:
	print('No valid input')
	sys.exit()





	
sleep(1)


print('Compiling the sketches. This can take a loOong time on slow raspberries. Time to get a coffee or a tea.')
arduinocompile()

print('\n \n \nDo you want to delete the downloaded files? \n ' + f_arduinotar + '\n ' + f_nicoshid)
yesno = raw_input('Type "YES" or "NO"  ')
if (yesno == 'YES'):
	rm(f_nicoshid)
	rm(f_arduinotar)

sleep(1)

print('\n\nIf you are using this program for the first time, you should install the keyboardmouse layout and restart the system. You must then reconfigure the input device. On the "Configure Input" screen hold down R1 in the input window and press X or Y.')

print('\nWould you install the keyboardmouse layout and restart the system?')
yesno = raw_input('Type "YES" or "NO"  ')
if (yesno == 'YES'):
	hexfile = d_precsb + '/MouseKeyboard-1.hex'
	if not os.path.isfile(hexfile):
		print('No ' + hexfile + ' found')
		print("Have a nice day")
		sys.exit()
	
	flashcommand = 'sh flash.sh ' + hexfile
	#print(flashcommand)
	os.system(flashcommand)
	sleep(1)
	rebootcommand = 'sudo reboot'
	os.system(rebootcommand)
else:
	print('Installation done \n \n Have a nice day')



#tar xfv arduino-1.8.5-linuxarm.tar.xz