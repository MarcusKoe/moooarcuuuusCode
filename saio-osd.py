#!/usr/bin/env python
#sudo apt-get install python-serial

# 
# This file originates from Kite's Super AIO control board project.
# Author: Kite (Giles Burgess)
# 
# THIS HEADER MUST REMAIN WITH THIS FILE AT ALL TIMES
#
# This firmware is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This firmware is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this repo. If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO 
import time
import os,signal,sys
import serial
import subprocess
import re
import logging
import logging.handlers
import stat
#import os
#import stat

try:
  from configparser import ConfigParser
except ImportError:
  from ConfigParser import ConfigParser  # ver. < 3.0

# Config variables
bin_dir         = '/home/pi/Super-AIO/release/saio/'
ini_data_file   = bin_dir + 'osd/data.ini'
ini_config_file = bin_dir + 'osd/config.ini'
osd_path        = bin_dir + 'osd/saio-osd'
rfkill_path     = bin_dir + 'rfkill/rfkill'
config_file     = '/boot/config-saio.txt'

# Hardware variables
pi_lowb = 23
pi_shdn = 27
pi_overtemp = 26

#https://stackoverflow.com/questions/33685078/python-check-if-a-dev-disk-device-exists
def devexists(path):
  """Test whether a path exists.  Returns False for broken symbolic links"""
  try:
    os.stat(path)
  except OSError:
    return False
  return True

serport = ""
for i in xrange(10):
  if (devexists('/dev/ttyACM' + str(i))):
    serport = '/dev/ttyACM' + str(i)
    print(serport)


# Software variables
settings_shutdown = 1 #Enable ability to shut down system

# Setup
logging.basicConfig(level=logging.DEBUG)
logging.info("Program Started")

# Init GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pi_lowb, GPIO.IN)
GPIO.setup(pi_shdn, GPIO.IN)
GPIO.setup(pi_overtemp, GPIO.OUT)
GPIO.output(pi_overtemp, GPIO.HIGH)

# Batt variables
voltscale = 203.5 #ADJUST THIS
currscale = 640.0
resdivmul = 4.0
resdivval = 1000.0
dacres = 33.0
dacmax = 1023.0

batt_threshold = 4
batt_low = 330
batt_shdn = 320
batt_islow = False

temperature_max = 60.0
temperature_threshold = 5.0
temperature_isover = False

# Wifi variables
wifi_state = 'UNKNOWN'
wifi_off = 0
wifi_warning = 1
wifi_error = 2
wifi_1bar = 3
wifi_2bar = 4
wifi_3bar = 5

# Set up a port
try:
  ser = serial.Serial(
    port=serport,
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
  )
except Exception as e:
  logging.exception("ERROR: Failed to open serial port");
  sys.exit(1);
  
# Set up configOSD file
configOSD = ConfigParser()
configOSD.add_section('protocol')
configOSD.set('protocol', 'version', 1)
configOSD.add_section('data')
configOSD.set('data', 'voltage', '-.--')
configOSD.set('data', 'temperature', '--.-')
configOSD.set('data', 'showdebug', 1)
configOSD.set('data', 'showwifi', 0)
configOSD.set('data', 'showmute', 0)

try:
  with open(ini_data_file, 'w') as configfile:
    configOSD.write(configfile)
except Expection as e:
  logging.exception("ERROR: Failed to create configOSD file");
  sys.exit(1);
    
# Set up OSD service
try:
  osd_proc = subprocess.Popen([osd_path, "-d", ini_data_file, "-c", ini_config_file])
  time.sleep(1)
  osd_poll = osd_proc.poll()
  if (osd_poll):
    logging.error("ERROR: Failed to start OSD, got return code [" + str(osd_poll) + "]\n")
    sys.exit(1)
except Exception as e:
  logging.exception("ERROR: Failed start OSD binary");
  sys.exit(1);

# Class to fake a section header for configparser
class FakeSecHead(object):
  def __init__(self, fp):
    self.fp = fp
    self.sechead = '[main]\n'

  def readline(self):
    if self.sechead:
      try: 
        return self.sechead
      finally: 
        self.sechead = None
    else: 
      return self.fp.readline()

# Set up a settings config file
configMAIN = ConfigParser()
if (os.path.isfile(config_file)):
  try:
    configMAIN = ConfigParser()
    configMAIN.readfp(FakeSecHead(open(config_file)))
    
    # Analyse values
    if (configMAIN.get('main', 'mode') == "TESTER" ):
      settings_shutdown = 0
    
  except Exception as e:
    logging.exception("ERROR: could not load configMAIN file");
else:
  logging.warning("WARNING: Failed to find configMAIN file");

# Check for shutdown state
def checkShdn():
  state = not GPIO.input(pi_shdn)
  if (state):
    logging.info("SHUTDOWN")
    doShutdown()

# Check for lowb state
def checkLowb():
  state = GPIO.input(pi_lowb)

# Read voltage
def readVoltage():
  ser.write('V')
  voltVal = int(ser.readline().rstrip('\r\n'))
  volt = int((( voltVal * voltscale * dacres + ( dacmax * 5 ) ) / (( dacres * resdivval ) / resdivmul)))
  
  logging.info("VoltVal [" + str(voltVal) + "]")
  logging.info("Volt    [" + str(volt) + "]V")
  
  global batt_islow
  
  if (batt_islow):
    if (volt > batt_low + batt_threshold):
      batt_islow = False
      logging.info("BATT OK")
    if (volt < batt_shdn):
      logging.info("VERY LOW BATT")
      #doShutdown()
      
  else:
    if (volt < batt_low):
      batt_islow = True
      logging.info("LOW BATT")
  
  return volt

# Get voltage percent
def getVoltagepercent(volt):
  return clamp(int( float(volt - batt_shdn)/float(420 - batt_shdn)*100 ), 0, 100)

# Read current
def readCurrent():
  ser.write('C')
  currVal = int(ser.readline().rstrip('\r\n'))
  curr = int((currVal * (dacres / (dacmax*10)) * currscale))
  
  logging.info("CurrVal [" + str(currVal) + "]")
  logging.info("Curr    [" + str(curr) + "]mA")
  return curr

# Read mode
def readModeDebug():
  ser.write('i')
  debugVal = int(ser.readline().rstrip('\r\n'))
  logging.info("Info    [" + str(debugVal) + "]")
  return debugVal

# Read wifi
def readModeWifi():
  ret = wifi_off
  
  ser.write('w')
  wifiVal = int(ser.readline().rstrip('\r\n'))
  logging.info("Wifi    [" + str(wifiVal) + "]")
  
  global wifi_state
  
  if (wifiVal):
    if (wifi_state != 'ON'):
      wifi_state = 'ON'
      logging.info("Wifi    [ENABLING]")
      try:
        out = subprocess.check_output([ 'sudo', rfkill_path, 'unblock', 'wifi' ])
        logging.info("Wifi    [" + str(out) + "]")
        out = subprocess.check_output([ 'sudo', rfkill_path, 'unblock', 'bluetooth' ])
        logging.info("BT      [" + str(out) + "]")
      except Exception, e:
        logging.info("Wifi    : " + str(e.output))
      ret = wifi_warning
    else:
      # Get signal strength
      raw = subprocess.check_output([ 'cat', '/proc/net/wireless'] )
      strengthObj = re.search( r'.wlan0: \d*\s*(\d*)\.\s*[-]?(\d*)\.', raw, re.I )
      if strengthObj:
        strength = 0
        if (int(strengthObj.group(1)) > 0):
          strength = int(strengthObj.group(1))
        elif (int(strengthObj.group(2)) > 0):
          strength = int(strengthObj.group(2))
        logging.info("Wifi    [" + str(strength) + "]strength")
        if (strength > 55):
          ret = wifi_3bar
        elif (strength > 40):
          ret = wifi_2bar
        elif (strength > 5):
          ret = wifi_1bar
        else:
          ret = wifi_warning
      else:
        logging.info("Wifi    [---]strength")
        ret = wifi_error
  else:
    if (wifi_state != 'OFF'):
      wifi_state = 'OFF'
      logging.info("Wifi    [DISABLING]")
      try:
        out = subprocess.check_output([ 'sudo', rfkill_path, 'block', 'wifi' ])
        logging.info("Wifi    [" + str(out) + "]")
        out = subprocess.check_output([ 'sudo', rfkill_path, 'block', 'bluetooth' ])
        logging.info("BT      [" + str(out) + "]")
      except Exception, e:
        logging.info("Wifi    : " + str(e.output))
      ret = wifi_error
  
  return ret

# Read mute
def readModeMute():
  ser.write('a')
  audVal = int(ser.readline().rstrip('\r\n'))
  logging.info("Audio   [" + str(audVal) + "]")
  if (audVal):
    return 0
  else:
    return 1

# Read CPU temp
def getCPUtemperature():
  res = os.popen('vcgencmd measure_temp').readline()
  return float(res.replace("temp=","").replace("'C\n",""))

# Check temp
def checkTemperature():
  temp = getCPUtemperature()
  
  global temperature_isover
  
  if (temperature_isover):
    if (temp < temperature_max - temperature_threshold):
      temperature_isover = False
      GPIO.output(pi_overtemp, GPIO.HIGH)
      logging.info("TEMP OK")
  else:
    if (temp > temperature_max):
      temperature_isover = True
      GPIO.output(pi_overtemp, GPIO.LOW)
      logging.info("OVERTEMP")
  return temp

# Do a shutdown
def doShutdown():
  os.system("sudo shutdown -h now")
  try:
    sys.stdout.close()
  except:
    pass
  try:
    sys.stderr.close()
  except:
    pass
  sys.exit(0)

# Create ini configOSD
def createINI(volt, curr, temp, debug, wifi, mute, file):
  #configOSD.set('data', 'voltage', '{0:.2f}'.format(volt/100.00))
  configOSD.set('data', 'voltage', volt)
  configOSD.set('data', 'temperature', temp)
  configOSD.set('data', 'showdebug', debug)
  configOSD.set('data', 'showwifi', wifi)
  configOSD.set('data', 'showmute', mute)

  with open(ini_data_file, 'w') as configfile:
    configOSD.write(configfile)
  
  osd_proc.send_signal(signal.SIGUSR1)

# Show MP4 overlay
def doVidOverlay(overlay):
  os.system("/usr/bin/omxplayer --no-osd --layer 999999 " + overlay + " --alpha 160;");

# Show PNG overlay
def doPngOverlay(overlay):
  try:
    os.system("kill -s 9 `pidof pngview`");
  except:
    pass
  try:
    os.system("./pngview -b 0 -l 999999 " + overlay + "&");
  except:
    pass

# Misc functions
def clamp(n, minn, maxn):
  return max(min(maxn, n), minn)

# Main loop
try:
  print "STARTED!"
  while 1:
    
    if (settings_shutdown):
      checkShdn()
    
    volt = readVoltage()
    temp = checkTemperature()
    debug = readModeDebug()
    wifi = readModeWifi()
    mute = readModeMute()    

    createINI(volt, 0, temp, debug, wifi, mute, ini_data_file)
    
    time.sleep(3);
  
except KeyboardInterrupt:
  GPIO.cleanup
  osd_proc.terminate()
