#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
from time import sleep as sleep
from RPi import GPIO as GPIO 
import time
import subprocess
from pythonfunctions import mkdir as mkdir
from pythonfunctions import find as find

from ConfigParser import SafeConfigParser


GPIO.cleanup()

count = -1
selection = ""

d_bse = '/home/pi/moooarcuuuusCode'
f_conf = os.path.join(d_bse, 'configuration.ini')
b_pngv = os.path.join(d_bse, 'pngview')
b_flsh = os.path.join(d_bse, 'flash.sh')
d_imgs = os.path.join(d_bse, 'images')
f_fimg = os.path.join(d_imgs, 'flashing.png')
f_styt = os.path.join(d_imgs, 'staytuned.png')

os.system('chmod +x ' + b_flsh)

if not (os.path.exists(d_imgs)):
	mkdir(d_imgs)

parser = SafeConfigParser()
parser.read(f_conf)

boardversion = parser.get('general', 'boardversion')
d_prec = os.path.join(d_bse, 'arduino-precompiled-selectbutton', boardversion)
xsize = parser.get('general', 'xres')
ysize = parser.get('general', 'yres')

screenres = xsize + 'x' + ysize
#print(d_prec)


b_selec = 24
b_flash = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(b_selec, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(b_flash, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def generateimage(strg, targetfile):
	if not (os.path.isfile(f_styt)):
		os.system('convert -size ' + screenres + ' -gravity Center label:"Please Wait... Generating Image :)" ' + f_styt)
	
	os.system(b_pngv + ' ' + '-b 0 -l 999999 ' + f_styt + ' &')
	os.system('convert -size ' + screenres + ' -gravity Center label:"' + strg + '" ' + targetfile)
	os.system('killall pngview')


def SelectButton(channel):


	print('Pressed Selectbutton')
	global count
	global selection
	
	count += 1
	print(count)

	files = find(d_prec, 0, 100)
	
	if (count >= len(files)-1) :
		count = -1
	
	#print(files)
	fvals = []
	for f in files:
		if not f.endswith('.hex'):
			print('No .hex file')
			sys.exit()
		fname = os.path.basename(f)
		#print(fname)
		targetfile = os.path.join(d_imgs, fname + '.png')
		fvals.append([f, fname, targetfile])
		if not (os.path.isfile(targetfile)):
			generateimage(fname, targetfile)

	
	hexfile = fvals[count][0]
	fname = fvals[count][1]
	picfile = fvals[count][2]
	
	selection = hexfile

	print(fname)
	
	os.system(b_pngv + ' ' + '-b 0 -l 999999 ' + picfile + ' &')
	
	
	starttime = int(time.time())
	runtime = 0
	while ( runtime <= 10 ):
		time.sleep(0.05)
		runtime = int(time.time()) - starttime
		if (GPIO.input(b_flash) == GPIO.LOW):
			
			print('starte Flashen')
			runtime = 11
			FlashArduino(hexfile)
		
		if (GPIO.input(b_selec) == GPIO.LOW):
			
			runtime = 11
	
	os.system('killall pngview')
	selection = ""
	






def FlashArduino(hexfile):
	
	os.system('killall pngview')
	os.system(b_flsh + ' ' + hexfile)
	sleep(1)

	

GPIO.add_event_detect(b_selec, GPIO.RISING, callback = SelectButton, bouncetime=200)


try:
	while True:

		sleep(5)

except KeyboardInterrupt:
	GPIO.cleanup()
	print("Time to say goodbye")
