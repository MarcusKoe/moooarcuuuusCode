import os
import string
import shutil
from ConfigParser import SafeConfigParser
import subprocess
import sys



def rm(source):
	if os.path.isfile(source) == True:
		os.remove(source)

def mkdir(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory)

def cp(source, target):
	shutil.copyfile(source, target)

def mv(source, target):
	shutil.move(source, target)

def find(path, start, stop):
	path = str(path)
	start = int(start)
	stop = int(stop)
	
	socket = len(string.split(path, '/')) - 1
	start = start + socket
	stop = stop + socket
	
	res = sum([[os.path.join(dirpath, filename) for filename in filenames] for dirpath, dirnames, filenames in os.walk(path) if start <= dirpath.count(os.sep) <= stop], [])
	return res


def rmdir(directory):
	files = find(directory, 0, 1000)
	for f in files:
		rm(f)
	shutil.rmtree(directory) 

def loadconfig():
	
	parser = SafeConfigParser()
	parser.read(getVars('f_conf'))
	bvers = parser.get('general', 'boardversion')
	xres = parser.get('general', 'xres')
	yres = parser.get('general', 'yres')
	return(bvers, xres, yres)


def getflashfile(portbutton, fname, bvers, xres, yres):
	
	res=os.path.join(portbutton, bvers, xres + 'x' + yres, fname)
	return(res)

def getVars(slc):
	
	httpArduino = 'https://downloads.arduino.cc/arduino-1.8.5-linuxarm.tar.xz'
	httpNicosHID = 'https://github.com/NicoHood/HID/archive/2.4.4.tar.gz'
	
	d_usr = '/home/pi'
	d_bse = os.path.join(d_usr, 'moooarcuuuusCode')
	f_arduinotar = os.path.join(d_bse, 'arduino-1.8.5-linuxarm.tar.xz')
	f_conf = os.path.join(d_bse, 'configuration.ini')
	d_ardupath = os.path.join(d_bse, 'arduino-1.8.5')
	d_ardulibaries = os.path.join(d_ardupath, 'libraries')
	f_arduexec = os.path.join(d_ardupath, 'arduino')
	d_buildpath = os.path.join('/dev', 'shm', 'arduinocompile')
	fn_nicoshidtar = 'HID-2.4.4.tar.gz'
	f_nicoshid = os.path.join(d_bse, fn_nicoshidtar)
	f_nicoshidlibs = os.path.join(d_ardupath, 'libraries', fn_nicoshidtar)
	
	d_arduinoconfig = os.path.join(d_bse, 'arduinosources' , 'configs')
	d_arduinosketches = os.path.join(d_bse, 'arduinosources' , 'sketches')
	
	d_precsb = os.path.join(d_bse, 'arduino-precompiled-selectbutton')
	d_precpt = os.path.join(d_bse, 'arduino-precompiled-ports')
	d_images = os.path.join(d_bse, 'images')
	
	f_flashsh = os.path.join(d_bse, 'flash.sh')
	f_pngview = os.path.join(d_bse, 'pngview')
	
	retc = None
	if slc is "httpArduino":
		retc = httpArduino
	if slc is "httpNicosHID":
		retc = httpNicosHID
	
	if slc is "d_usr":
		retc = d_usr
	if slc is "d_bse":
		retc = d_bse
	if slc is "f_arduinotar":
		retc = f_arduinotar
	if slc is "f_conf":
		retc = f_conf
	if slc is "d_ardupath":
		retc = d_ardupath
	if slc is "d_ardulibaries":
		retc = d_ardulibaries
	if slc is "f_arduexec":
		retc = f_arduexec
	if slc is "d_buildpath":
		retc = d_buildpath
	if slc is "f_nicoshid":
		retc = f_nicoshid
	if slc is "f_nicoshidlibs":
		retc = f_nicoshidlibs
	if slc is "d_arduinoconfig":
		retc = d_arduinoconfig
	if slc is "d_arduinosketches":
		retc = d_arduinosketches
	if slc is "d_precsb":
		retc = d_precsb
	if slc is "d_precpt":
		retc = d_precpt
	if slc is "d_images":
		retc = d_images
	if slc is "f_flashsh":
		retc = f_flashsh
	if slc is "f_pngview":
		retc = f_pngview


	return(retc)


def viewpng(image=None):
	d_images = getVars('d_images')
	f_pngview = getVars('f_pngview')
	os.system('chmod +x ' + f_pngview)
	os.system('killall pngview')
	if image is 'compiling':
		bvers, xres, yres = loadconfig()
		f_image = os.path.join(d_images, 'compile-' + xres + '.png')
		os.system(f_pngview + ' ' + '-b 0 -l 999999 ' + f_image + ' &')
	

def arduinocompile():
	
	Layout_ports = ['StandardGamepad-1', 'MouseKeyboard-1']
	
	f_arduexec = getVars('f_arduexec')
	d_buildpath = getVars('d_buildpath')
	d_arduinoconfig = getVars('d_arduinoconfig')
	d_arduinosketches = getVars('d_arduinosketches')
	d_precsb = getVars('d_precsb')
	d_precpt = getVars('d_precpt')
	
	if not os.path.isdir(d_precsb):
		mkdir(d_precsb)
	if not os.path.isdir(d_precpt):
		mkdir(d_precpt)
	

	bvers, xres, yres = loadconfig()
	sketchdirs = {}
	print(d_arduinosketches)
	fls = find(d_arduinosketches, 0, 10)
	for f in fls:
		dname = os.path.basename(os.path.dirname(f))
		sketchdirs[dname] = 1
		#print(f, dname)
	
	for sketchname in sketchdirs.keys():
		
		if os.path.isdir(d_buildpath):
			rmdir(d_buildpath)
		#print(d_buildpath)
		mkdir(d_buildpath)
		
		#print(sketchname)
		d_sketch = os.path.join(d_arduinosketches, sketchname)
		f_sketch = os.path.join(d_sketch, sketchname + '.ino')

		#f_hexfile = sketchname + '.ino.hex'
		f_sourcehexfile = os.path.join(d_buildpath, sketchname + '.ino.hex')
		#print(f_sourcehexfile)
		f_targethexfile = os.path.join(d_precsb, sketchname + '.hex')
		f_targethexfile_ports = os.path.join(d_precpt, sketchname + '.hex')
		if os.path.isfile(f_targethexfile):
			
			print(sketchname + ' is already compiled')
			viewpng()
			
		else:

			viewpng('compiling')
			f_sourceconfig = os.path.join(d_arduinoconfig, xres + '-' + bvers +'-config.h')
			f_targetconfig = os.path.join(d_sketch, 'config.h')
			
			if os.path.isfile(f_targetconfig):
				#print('Delete Config')
				rm(f_targetconfig)
			if not os.path.isfile(f_sourceconfig):
				print('No source configuration for you configuration found')
				print("Have a nice day")
				sys.exit()
			cp(f_sourceconfig, f_targetconfig)
			
			print('Compiling ' + sketchname)
			arduinotest = f_arduexec + ' --verify --board arduino:avr:leonardo --pref build.path=' + d_buildpath + ' ' +  f_sketch
			#print(arduinotest)
			p=(subprocess.call(arduinotest, shell=True, stderr=subprocess.PIPE))
			if not p == 0:
				print('Compile process failed')
				print("Have a nice day")
				sys.exit()
			cp(f_sourcehexfile, f_targethexfile)
			if sketchname in Layout_ports:
				print("Kopiere datei in Ports")
				print("cp(" + f_sourcehexfile + ', ' + f_targethexfile_ports + ')')
				cp(f_sourcehexfile, f_targethexfile_ports)
			viewpng()

		