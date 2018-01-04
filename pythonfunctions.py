import os
import string
import shutil

def rm(source):
	if os.path.isfile(source) == True:
		os.remove(source)

def mkdir(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory) 

def find(path, start, stop):
	path = str(path)
	start = int(start)
	stopp = int(stop)
	
	socket = len(string.split(path, '/')) - 1
	start = start + socket
	stopp = stop + socket
	
	res = sum([[os.path.join(dirpath, filename) for filename in filenames] for dirpath, dirnames, filenames in os.walk(path) if start <= dirpath.count(os.sep) <= stop], [])
	return res


def rmdir(directory):
	files = find(directory, 0, 1000)
	for f in files:
		rm(f)
	shutil.rmtree(directory) 