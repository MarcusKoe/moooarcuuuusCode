# moooarcuuuusCode


https://www.sudomod.com/forum/viewtopic.php?f=51&p=52659

install:
cd && git clone https://github.com/MarcusKoe/moooarcuuuusCode.git && cd moooarcuuuusCode & python setup.py

update:
cd && cd moooarcuuuusCode && git pull && python setup.py

Mousemode for Kites SAIO. Tested adventures with scummvm: Monkey island 1 + 2, Sam and Max, Broken Sword, Simon the Sorcerer 1 + 2


Changes:

05. 01. 2018
SAIO_v2a-MouseKeyboard.ino
Added screensaver, after 240 seconds (4 min) no button press, the screen backlight fades out
Double button X in joystick mode (Y was useless)
Select is now "left_ctrl + F5" -> global options menu from scummvm
Little improvement in the config mechanism

SAIO_v2a.ino
Added configuration mode and screensaver


DukeNukem.ino
Added DukeNukem layout