# FLASH ATMEGA32u4 WITH HEX
#
# Author: Giles Burgess
# GitHub: https://github.com/geebles/Super-AIO
#
# reset.py from https://github.com/nicholaskell/Arduino_Loader
#
# Run with ./flash.sh hexfile.hex
#

bsd="/home/pi/moooarcuuuusCode"

# Arguments check
if [ "$#" -ne 1 ]; then
  echo "Usage: ./flash.sh <hexfile>"
  exit 1
fi

# Config
HEX=$1



# Hex existence check
if [ ! -e $HEX ]; then
  echo "ERROR: Hex file doesn't exist"
  exit 1
fi

# AVRDUDE existence check
if [ ! -e `which avrdude` ]; then
  echo "ERROR: avrdude does not exist in PATH"
  exit 1
fi

OSDPID=$(pgrep saio-osd)
#sleep 1
kill -2 $OSDPID
sleep 2

avrdudereturn="666"
while [ $avrdudereturn != 0 ] ; do

	for i in $(seq 0 10) ; do

		if [ -e "/dev/ttyACM"$i ] ; then 
			echo "PORT=/dev/ttyACM"$i
			PORT="/dev/ttyACM"$i
		fi 

	done

	
	
	# Enter board into bootloader mode
	python $bsd/reset.py $PORT
	ret=$?
	if [ $ret != 0 ]; then
	printf "Error while trying to reset MCU [$ret]"
	exit $ret
	fi
	
	# Sleep a little bit
	sleep 5
	
	# Flash the hex!
	avrdude -P $PORT -c avr109 -p atmega32u4 -b 57600 -U flash:w:$HEX:i
	ret=$?
	avrdudereturn=$ret
	
	if [ $avrdudereturn != 0 ]; then
	printf "Error while trying to flash MCU [$ret]"
	fi
	
	sleep 5

done

/usr/bin/nice -n 19 /usr/bin/ionice -c3 python /home/pi/moooarcuuuusCode/saio-osd.py > /dev/null 2>&1 &

sleep 1

#python reset.py $PORT