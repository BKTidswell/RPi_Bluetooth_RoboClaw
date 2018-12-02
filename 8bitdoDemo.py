#import evdev
from evdev import InputDevice, categorize, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')

#button code variables (change to suit your device)
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308

x = 0
y = 1

up = 0
down = 255
left = 0
right = 255

start = 315
select = 314

lTrig = 311
rTrig = 310

#prints out device info at start
print(gamepad)

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
	if event.type == ecodes.EV_KEY:
		if event.value == 1:
            		if event.code == yBtn:
                		print("Y")
            		elif event.code == bBtn:
                		print("B")
            		elif event.code == aBtn:
                		print("A")
            		elif event.code == xBtn:
                		print("X")

	    		elif event.code == start:
                		print("start")
            		elif event.code == select:
                		print("select")

            		elif event.code == lTrig:
                		print("left bumper")
            		elif event.code == rTrig:
             	 		print("right bumper")
   
	elif event.type == ecodes.EV_ABS:    
    		if event.code == y:
	    		if event.value == up:
            			print("up")
	    		elif event.value == down:
	        		print("down")
        	elif event.code == x:
            		if event.value == left:
                		print("left")
            		elif event.value == right:
                		print("right")
