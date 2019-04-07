import time
from roboclaw import Roboclaw
from evdev import InputDevice, categorize, ecodes
import fnmatch
import os

#
#Controller Specifications
# D-pad:
#	Right = Right
#	Down = Change control mode
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
#  3 ___ 2

rc1Num = 0
rc2Num = 1

#rc1Address = '/dev/ttyACM0'
#rc2Address = '/dev/ttyACM1'

#creates object 'gamepad' to store the data
gamepadConnect = False
while(not gamepadConnect):
	try:
		gamepad = InputDevice('/dev/input/event0')
		gamepadConnect = True
	except:
		print("No Gamepad Connected. Please turn it on!")
		time.sleep(0.5)

#Opens up roboclaw inputs

address = 0x80

#button code variables as found for 8bitdo gamepad
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308

start = 315
select = 314

lTrig = 310
rTrig = 311

#These aren't button numbers but are used for the D-pad
# which uses a different system
x = 0
y = 1

up = 0
down = 255
left = 0
right = 255
middle = 127

#prints out device info at start
print(gamepad)

#defines full speed
spdMax = 63

#defines motor positions
topM = 3
rightM = 1
leftM = 2

#Used for hold-to-use motor control
lastPressed = "None"
buttonDict = {yBtn:"Y",aBtn:"A",bBtn:"B",xBtn:"X"}

constRun = True #Will not change
revRun = False
sleepTime = 0.5

M1Dir = 1
M2Dir = -1
M3Dir = 1

#creates motor winding functions
#forwards

def rotateRight(topM,rightM,leftM):
	tempM = topM
	topM = rightM
	rightM = leftM
	leftM = tempM
	return(topM,rightM,leftM)
	
def rotateLeft(topM,rightM,leftM):
	tempM = topM
	topM = leftM
	leftM = rightM
	rightM = tempM
	return(topM,rightM,leftM)

def flushLoop():
	while gamepad.read_one() != None:
			pass

allowRotate = False

try:	
	for event in gamepad.read_loop():
		if event.type == ecodes.EV_KEY:
			if event.value == 1:
				if event.code == select:
					allowRotate = not allowRotate 
					#Motor Reset?
				elif event.code == lTrig:
					#Rotate Contact Left (Counterclock)
					if allowRotate:
						(topM,rightM,leftM) = rotateLeft(topM,rightM,leftM)
						allowRotate = False
				elif event.code == rTrig:
					#Rotate Contact Right (Clock)
					if allowRotate:
						(topM,rightM,leftM) = rotateRight(topM,rightM,leftM)
						allowRotate = False
				elif event.code == yBtn:
					#Turn Left
					if not revRun:
						pass
					else:
						print("Y")
						time.sleep(sleepTime*3)
						(topM,rightM,leftM) = rotateRight(topM,rightM,leftM)
					lastPressed = "Y"
				elif event.code == bBtn:
					#Inch
					print("B")
					time.sleep(sleepTime*3)
					lastPressed = "B"
				elif event.code == aBtn:
					#Crunch
					if not revRun:
						print("A+")
					else:
						print("A-")
					time.sleep(sleepTime*1)
					lastPressed = "A"
				elif event.code == xBtn:
					#Turn Right
					if not revRun:
						pass
					else:
						print("X")
						time.sleep(sleepTime*4)
						(topM,rightM,leftM) = rotateLeft(topM,rightM,leftM)
					lastPressed = "X"
					
		if event.value == 0 and event.code in buttonDict.keys() and not constRun:
			if lastPressed == buttonDict[event.code]:
				lastPressed = "None"
				stopAll()
				
		elif event.type == ecodes.EV_ABS:    
			if event.code == y:
				if event.value == up:
					#Lift
					print("Up")
					lastPressed = "up"
				elif event.value == down:
					revRun = not revRun
					if revRun:
						print("Motors Unwinding")
					else:
						print("Motors Winding")
			elif event.code == x:	
				if event.value == left:
					#Move Left
					print("Left")
					lastPressed = "left"
				elif event.value == right:
					#Move Right
					print("Right")
					lastPressed = "right"
		
		if lastPressed not in ["None","up","left","right"]:
			lastPressed = "None"
			time.sleep(sleepTime)
		
		flushLoop()
			
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	pass	   


