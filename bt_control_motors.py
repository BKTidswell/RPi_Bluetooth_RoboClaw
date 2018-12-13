import time
from roboclaw import Roboclaw
from evdev import InputDevice, categorize, ecodes

#Controller Specifications
# D-pad:
#	Right = Right
#	Down = ?????
#	Left = Left
#	Up = Lift
# Buttons:
#	A = Unwind
#	B = Inch (hold to wind)
#	Y = Turn Left
#	X = Turn Right
#	Start = Emergency Stop
#	Select = Motor Reset
# Bumpers:
#	Right = Rotate Contact Right
#	Left = Rotate Contact Left

# Motor Diagram
#     1
#   /   \
#  3_____2


#creates object 'gamepad' to store the data
gamepad = InputDevice('/dev/input/event0')

#Opens up roboclaw inputs
rc1 = Roboclaw("/dev/ttyACM0",9600)
rc2 = Roboclaw("/dev/ttyACM1",9600)

rc1.Open()
rc2.Open()

address = 0x80

#button code variables as found for 8bitdo gamepad
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308

start = 315
select = 314

lTrig = 311
rTrig = 310

#These aren't button numbers but are used for the D-pad
# which uses a different system
x = 0
y = 1

up = 0
down = 255
left = 0
right = 255

#prints out device info at start
print(gamepad)

#defines full speed
spdMax = 127

#defines motor positions
top = 1
right = 2
left = 3

#creates motor winding functions
#forwards
def motorWind(mNum,speed):
	if mNum = 1:
		rc1.ForwardM1(address,speed*spdMax)
	elif mNum = 2:
		rc1.ForwardM2(address,speed*spdMax)
	elif mNum = 3:
		rc2.ForwardM1(address,speed*spdMax)
	else:
		print("Incorrect Motor Number")

#backwards
def motorUnwind(mNum,speed):
	if mNum = 1:
		rc1.BackwardM1(address,speed*spdMax)
	elif mNum = 2:
		rc1.BackwardM2(address,speed*spdMax)
	elif mNum = 3:
		rc2.BackwardM1(address,speed*spdMax)
	else:
		print("Incorrect Motor Number")

#stopped
def motorStop(nNum):
	if mNum = 1:
		rc1.ForwardM1(address,0)
	elif mNum = 2:
		rc1.ForwardM2(address,0)
	elif mNum = 3:
		rc2.ForwardM1(address,0)
	else:
		print("Incorrect Motor Number")

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
	if event.type == ecodes.EV_KEY:
		if event.value == 1:
            if event.code == yBtn:
            	#Turn Left
                print("Y")
            elif event.code == bBtn:
            	#Inch
                print("B")
            elif event.code == aBtn
            	#Unwind
                print("A")
            elif event.code == xBtn:
            	#Turn Right
                print("X")

	    		elif event.code == start:
	    				#E-Stop
	    				motorStop(top)
	    				motorStop(right)
	    				motorStop(left)
                		print("start")
            	elif event.code == select:
            			#Motor Reset?
                		print("select")

            		elif event.code == lTrig:
            			#Rotate Contact Left
                		print("left bumper")
            		elif event.code == rTrig:
            			#Rotate Contact Right
             	 		print("right bumper")
   
	elif event.type == ecodes.EV_ABS:    
    		if event.code == y:
	    		if event.value == up:
	    			#Lift
            		print("up")
	    		elif event.value == down:
	    			#?????
	        		print("down")
        	elif event.code == x:
            	if event.value == left:
            		#Move Left
                	print("left")
            	elif event.value == right:
            		#Move Right
                	print("right")
   else:
   	   


