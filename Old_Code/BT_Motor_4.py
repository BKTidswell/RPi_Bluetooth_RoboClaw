import time, threading
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
#     0
#   /   \
#  2 ___ 1

# Strings for motor connection
motorsConnect = False

#creates object 'gamepad' to store the data
gamepadConnect = False
while(not gamepadConnect):
	try:
		gamepad = InputDevice('/dev/input/event0')
		gamepadConnect = True
	except:
		print("No Gamepad Connected. Please turn it on!")
		time.sleep(0.5)

#sets up motor driver pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
numMotors = 3
IN1PINS = [18,12,23] #[8,12,18]
IN2PINS = [22,16,26] #[10,16,22]

#Makes the PMW references
IN1PWMS = [None for x in range(numMotors)]
IN2PWMS = [None for x in range(numMotors)]

#Starts all PWM at 0
for i in range(numMotors):
	pin = IN1PINS[i]
	GPIO.setup(pin,GPIO.OUT)
	IN1PWMS[i] = GPIO.PWM(pin,100)
	IN1PWMS[i].start(0)
	
for i in range(numMotors):
	pin = IN2PINS[i]
	GPIO.setup(pin,GPIO.OUT)
	IN2PWMS[i] = GPIO.PWM(pin,100)
	IN2PWMS[i].start(0)

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
#spdMax = 63
spdMax = 100 #32000

#defines motor positions
topM = 0
rightM = 1
leftM = 2

MDirs = [1,1,1]

#creates motor winding functions
#forwards

def motorControl(mNum,speed):
	if speed*MDirs[mNum] >= 0:
		IN1PWMS[mNum].ChangeDutyCycle(int(speed*spdMax*MDirs[mNum]))
		IN2PWMS[mNum].ChangeDutyCycle(0)
	else:
		IN1PWMS[mNum].ChangeDutyCycle(0)
		IN2PWMS[mNum].ChangeDutyCycle(int(abs(speed*spdMax*MDirs[mNum])))
	
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

#Used for hold-to-use motor control
lastPressed = "None"
buttonDict = {yBtn:"Y",aBtn:"A",bBtn:"B",xBtn:"X"}

constRun = True #Will not change
allowRotate = False
revRun = False

sleepTime = 0.75
tTime = 0.75

t = threading.Timer(0.01,stopAll)
t.start()

try:
	for event in gamepad.read_loop():
		if event.type == ecodes.EV_KEY:
			if event.value == 1:
				if event.code == start:
					#E-Stop
					stopAll()
					print("Start")
				elif event.code == select:
					allowRotate = not allowRotate 
					#Motor Reset?
					print("Select")
				elif event.code == lTrig:
					#Rotate Contact Left (Counterclock)
					if allowRotate:
						(topM,rightM,leftM) = rotateLeft(topM,rightM,leftM)
						allowRotate = False
					print("Left Trigger")
				elif event.code == rTrig:
					#Rotate Contact Right (Clock)
					if allowRotate:
						(topM,rightM,leftM) = rotateRight(topM,rightM,leftM)
						allowRotate = False
					print("Right Trigger")
				elif event.code == yBtn:
					#Turn Left
					if not revRun:
						t = threading.Timer(sleepTime*15,stopAll)
						t.start()
						motorControl(rightM,1)
						time.sleep(sleepTime*4)
						motorControl(leftM,1)
						time.sleep(sleepTime*4)
						motorControl(rightM,-1)
						time.sleep(sleepTime*2.25)
						motorControl(leftM,-1)
						time.sleep(sleepTime*3.75)
						(topM,rightM,leftM) = rotateRight(topM,rightM,leftM)
						t.cancel()
					else:
						pass
					print("Y")
					lastPressed = "Y"
				elif event.code == bBtn:
					#Inch
					#motorControl(topM,-1)
					t = threading.Timer(sleepTime*6.5,stopAll)
					t.start()
					motorControl(rightM,1)
					motorControl(leftM,1)
					time.sleep(sleepTime*4)
					#motorControl(topM,1)
					motorControl(rightM,-1)
					motorControl(leftM,-1)
					time.sleep(sleepTime*1.5)
					t.cancel()
					print("B")
					lastPressed = "B"
				elif event.code == aBtn:
					#Crunch
					if not revRun:
						t = threading.Timer(sleepTime*1.1,stopAll)
						t.start()
						motorControl(topM,1)
						motorControl(rightM,1)
						motorControl(leftM,1)
						time.sleep(sleepTime*1)
						t.cancel()
					else:
						t = threading.Timer(sleepTime*1,stopAll)
						t.start()
						motorControl(topM,-1)
						motorControl(rightM,-1)
						motorControl(leftM,-1)
						time.sleep(sleepTime*0.88)
						t.cancel()
					print("A")
					lastPressed = "A"
				elif event.code == xBtn:
					#Turn Right
					if not revRun:
						t = threading.Timer(sleepTime*11,stopAll)
						t.start()
						motorControl(leftM,1)
						time.sleep(sleepTime*3)
						motorControl(rightM,1)
						time.sleep(sleepTime*3)
						motorControl(leftM,-1)
						time.sleep(sleepTime*1.75)
						motorControl(rightM,-1)
						time.sleep(sleepTime*2.5)
						(topM,rightM,leftM) = rotateLeft(topM,rightM,leftM)
						t.cancel()
					else:
						pass
					print("X")
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
					print("Up")
				elif event.value == down:
					revRun = not revRun
					if revRun:
						print("Motors Unwinding")
					else:
						print("Motors Winding")
					t = threading.Timer(tTime,stopAll)
					t.start()
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
					print("Left")
				elif event.value == right:
					#Move Right
					if not revRun:
						motorControl(rightM,1)
					else:
						motorControl(rightM,-1)
					lastPressed = "right"
					t = threading.Timer(tTime,stopAll)
					t.start()
					print("Right")
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
