import time, threading
from roboclaw import Roboclaw
from evdev import InputDevice, categorize, ecodes
import fnmatch
import os
import RPi.GPIO as GPIO

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

# Strings for motor connection
motorsConnect = False

while(not motorsConnect):
	try:
		driverFiles = []

		for file in os.listdir('/dev/'): 
         		if fnmatch.fnmatch(file,'ttyACM*'):
                		driverFiles.append("/dev/"+file)

		rc1Address = driverFiles[rc1Num]
		rc2Address = driverFiles[rc2Num]

		#Opens up roboclaw inputs
		rc1 = Roboclaw(rc1Address,9600)
		rc2 = Roboclaw(rc2Address,9600)

		rc1.Open()
		rc2.Open()

		motorsConnect = True
	except:
		print("Connect Both Motor Drivers")
		time.sleep(0.5)

print(rc1Address)
print(rc2Address)

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

rc1 = Roboclaw(rc1Address,9600)
rc2 = Roboclaw(rc2Address,9600)

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

#Sets up LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.OUT)
GPIO.output(14,GPIO.HIGH)

#creates motor winding functions
#forwards

def motorControl(mNum,speed):
	if mNum == 1:
		rc1.ForwardBackwardM1(address,64+int(speed*spdMax*M1Dir))
	elif mNum == 2:
		rc1.ForwardBackwardM2(address,64+int(speed*spdMax*M2Dir))
	elif mNum == 3:
		rc2.ForwardBackwardM1(address,64+int(speed*spdMax*M3Dir))
	else:
		print("Incorrect Motor Number")

def stopAll():
	motorControl(topM,0)
	motorControl(rightM,0)
	motorControl(leftM,0)

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
		
def current_milli_time():
	return int(round(time.time() * 1000))

allowRotate = False
tTime = 1

try:
	for event in gamepad.read_loop():
		if event.type == ecodes.EV_KEY:
			if event.value == 1:
				if event.code == start:
					#E-Stop
					stopAll()
				elif event.code == select:
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
						motorControl(rightM,1)
						time.sleep(sleepTime*3)
						motorControl(leftM,1)
						time.sleep(sleepTime*3)
						motorControl(rightM,-1)
						time.sleep(sleepTime*4)
						motorControl(leftM,-1)
						time.sleep(sleepTime*4)
						(topM,rightM,leftM) = rotateRight(topM,rightM,leftM)
					lastPressed = "Y"
				elif event.code == bBtn:
					#Inch
					#motorControl(topM,-1)
					motorControl(rightM,1)
					motorControl(leftM,1)
					time.sleep(sleepTime*4)
					#motorControl(topM,1)
					motorControl(rightM,-1)
					motorControl(leftM,-1)
					time.sleep(sleepTime*2.6)
					lastPressed = "B"
				elif event.code == aBtn:
					#Crunch
					if not revRun:
						motorControl(topM,1)
						motorControl(rightM,1)
						motorControl(leftM,1)
						time.sleep(sleepTime*1)
					else:
						motorControl(topM,-1)
						motorControl(rightM,-1)
						motorControl(leftM,-1)
						time.sleep(sleepTime*0.88)
					lastPressed = "A"
				elif event.code == xBtn:
					#Turn Right
					if not revRun:
						pass
					else:
						motorControl(leftM,1)
						time.sleep(sleepTime*3)
						motorControl(rightM,1)
						time.sleep(sleepTime*3)
						motorControl(leftM,-1)
						time.sleep(sleepTime*4)
						motorControl(rightM,-1)
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
					if not revRun:
						motorControl(topM,1)
					else:
						motorControl(topM,-1)
					lastPressed = "up"
					t = threading.Timer(tTime,stopAll)
					t.start()
				elif event.value == down:
					revRun = not revRun
					if revRun:
						print("Motors Unwinding")
						GPIO.output(14,GPIO.LOW)
					else:
						GPIO.out(14,GPIO.HIGH)
						print("Motors Winding")
				elif event.value == middle:
					stopAll()
					t.cancel()
			elif event.code == x:	
				if event.value == left:
					#Move Left
					if not revRun:
						motorControl(leftM,1)
					else:
						motorControl(leftM,-1)
					lastPressed = "left"
					t = threading.Timer(tTime,stopAll)
					t.start()
				elif event.value == right:
					#Move Right
					if not revRun:
						motorControl(rightM,1)
					else:
						motorControl(rightM,-1)
					lastPressed = "right"
					t = threading.Timer(tTime,stopAll)
					t.start()
				elif event.value == middle:
					stopAll()
					t.cancel()
		
		if lastPressed not in ["None","up","left","right"]:
			lastPressed = "None"
			time.sleep(sleepTime)
			stopAll()
			
		flushLoop()
			
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	stopAll()
	   


