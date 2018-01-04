#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
from time import sleep as sleep
import time
from pythonfunctions import mkdir as mkdir
from pythonfunctions import find as find

from ConfigParser import SafeConfigParser



d_bse = '/home/pi/moooarcuuuusCode'
f_conf = os.path.join(d_bse, 'configuration.ini')
b_flsh = os.path.join(d_bse, 'flash.sh')
os.system('chmod +x ' + b_flsh)

parser = SafeConfigParser()
parser.read(f_conf)

boardversion = parser.get('general', 'boardversion')
d_prec = os.path.join(d_bse, 'arduino-precompiled-selectbutton', boardversion)


files = find(d_prec, 0, 100)
for hexfile in files:
	if not hexfile.endswith('.hex'):
		print('No .hex file')
		sys.exit()
	content = '#!/bin/bash \n \n #generated by execute-ports-controllerflashing.py \n \n' + b_flsh + ' ' + hexfile
	fname = os.path.basename(hexfile)
	ports = '/home/pi/RetroPie/roms/ports'
	mkdir(ports)
	portfile = os.path.join(ports, fname + '.sh')
	if not os.path.isfile(portfile):
		with open(portfile, 'w') as pfile:
			pfile.write(content)
		print('Generate:')
		print(content)
		os.system('chmod +x ' + portfile)
	else:
		print('Executable file exists, skipping')
