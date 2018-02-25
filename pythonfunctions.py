import os
import string
import shutil
from ConfigParser import SafeConfigParser

def rm(source):
	if os.path.isfile(source) == True:
		os.remove(source)

def mkdir(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory) 

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

def loadconfig(configfile):
	parser = SafeConfigParser()
	parser.read(configfile)
	bvers = parser.get('general', 'boardversion')
	xres = parser.get('general', 'xres')
	yres = parser.get('general', 'yres')
	return(bvers, xres, yres)


def getflashfile(portbutton, fname, bvers, xres, yres):
	
	res=os.path.join(portbutton, bvers, xres + 'x' + yres, fname)
	return(res)