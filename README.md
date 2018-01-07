# moooarcuuuusCode...

...is a little set of scripts to flash the atmega32u4 on Kites SAIO board 0.5 and 0.6. 

For informations see:
https://www.sudomod.com/forum/viewtopic.php?f=51&p=52659

## install:

```
"cd"
"git clone https://github.com/MarcusKoe/moooarcuuuusCode.git"
"cd moooarcuuuusCode"
"python setup.py"
```

## update:

```
"cd"
"cd moooarcuuuusCode"
"git pull"
"python setup.py"
```

## Manuall install:

```
Put SD-Card in your computer
Download .zip file from Github (https://github.com/MarcusKoe/moooarcuuuusCode/archive/master.zip)
Copy master.zip to the sd-card in /home/pi
Plug USB-keyboard on the Gameboy and start the device
When ES is loaded, press F4 (starts a terminal)
"unzip master.zip"
"mv moooarcuuuusCode-master/ moooarcuuuusCode"
You can delete the .zip with "rm master.zip"
"cd moooarcuuuusCode"
"python setup.py"
```

Install avrdude manually:

```
"sudo dpkg -i libftdi1_0.20-2_armhf.deb avrdude_6.1-2+rpi1_armhf.deb"
```







## Conents:

### SAIO_v2a.ino
Original from Kite - with screensaver


### SAIO_v2a-MouseKeyboard.ino
Mousemode for Kites SAIO. Tested adventures in scummvm: Monkey island 1 + 2, Sam and Max, Broken Sword, Simon the Sorcerer 1 + 2. With screensaver


"Dpad mouse mode" with Released L1:

```
Dpad is left right up down
A - Enter
B - Escape
Y - Period (.)
X - Space
Start - Left ctrl
Select - Left shift
"Dpad mouse mode" with Pressed L1:
Dpad - Mousemove
A - Mouse right click
B - Mouse left click
Y - Period (.)
X - Escape
Start - Space
Select - F5 + Left ctrl (scummvm menu)
```


"Joystick mode"
```
Dpad is left right up down
Joystick is mouse
L1 - Mouse left click
R1 - Mouse right click
A - Enter
B - Escape
Y - Period (.)
X - M
Start - Space
Select - F5 + Left ctrl (scummvm menu)
```

Configuration:

```
Mode + L1 < 5sec
change mouse speed 1 - 5
Mode + R1 < 5sec
flip x and y axis
Mode + L1 > 5sec < 10sec
invert x axis
Mode + R1 > 5sec < 10sec
invert y axis
Mode + L1 > 10sec < 15 sec
change mouse mode, dpad or joystick
Mode + R1 > 10sec < 15 sec
screensaver on (or off), after 240 seconds (4 min) no button press, the screen backlight fades out
```

### DukeNukem.ino

```
DPad - Forward, Backward, Strafe left, Strafe right
Joystick mouselook
R1 fire
L1 jump
R2 run
L1 open/use
ABXY up down left right	(for main menu)
Start enter inventory or enter in menu	
Select escape (main menu)
```
