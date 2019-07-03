import time #, threading
from evdev import InputDevice, categorize, ecodes
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

#Used for hold-to-use motor control
lastPressed = "None"
buttonDict = {yBtn:"Y",aBtn:"A",bBtn:"B",xBtn:"X"}

constRun = True #Will not change
allowRotate = False
revRun = False

sleepTime = 0.5
tTime = 0.5

#creates motor winding functions
def motorControl(mNum,speed):
	if speed*MDirs[mNum] >= 0:
		IN1PWMS[mNum].ChangeDutyCycle(int(speed*spdMax*MDirs[mNum]))
		IN2PWMS[mNum].ChangeDutyCycle(0)
	else:
		IN1PWMS[mNum].ChangeDutyCycle(0)
		IN2PWMS[mNum].ChangeDutyCycle(int(abs(speed*spdMax*MDirs[mNum])))

#Allows easier running of longer patterns
def runMotorPattern(motors,speeds,delays):
	for i in range(len(motors)):
		motorControl(motors[i],speeds[i])
		time.sleep(sleepTime*delays[i])

#stops all motors
def stopAll():
	motorControl(topM,0)
	motorControl(rightM,0)
	motorControl(leftM,0)

#Changes the direction of the motors to the right
def rotateRight(topM,rightM,leftM):
	tempM = topM
	topM = rightM
	rightM = leftM
	leftM = tempM
	return(topM,rightM,leftM)

#Changes the direction of the motors to the left
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
					runMotorPattern([rightM,leftM,rightM,leftM],[1,1,-1,-1],[3,3,1,2])
					(topM,rightM,leftM) = rotateRight(topM,rightM,leftM)
					print("Y")
					lastPressed = "Y"
				elif event.code == xBtn:
					#Turn Right
					runMotorPattern([leftM,rightM,leftM,rightM],[1,1,-1,-1],[3,3,1,2])
					(topM,rightM,leftM) = rotateLeft(topM,rightM,leftM)
					print("X")
					lastPressed = "X"
				elif event.code == bBtn:
					#Inch
					runMotorPattern([rightM,leftM,rightM,leftM],[1,1,-1,-1],[0,3,0,1.25])
					print("B")
					lastPressed = "B"
				elif event.code == aBtn:
					#Crunch
					if not revRun:
						runMotorPattern([topM,rightM,leftM],[1,1,1],[0,0,1])
					else:
						runMotorPattern([topM,rightM,leftM],[-1,-1,-1],[0,0,0.75])
					print("A")
					lastPressed = "A"

					
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
					print("Up")
				elif event.value == down:
					revRun = not revRun
					if revRun:
						print("Motors Unwinding")
					else:
						print("Motors Winding")
				elif event.value == middle:
					stopAll()
			elif event.code == x:	
				if event.value == left:
					#Move Left
					if not revRun:
						motorControl(leftM,1)
					else:
						motorControl(leftM,-1)
					lastPressed = "left"
					print("Left")
				elif event.value == right:
					#Move Right
					if not revRun:
						motorControl(rightM,1)
					else:
						motorControl(rightM,-1)
					lastPressed = "right"
					print("Right")
				elif event.value == middle:
					stopAll()
		
		if lastPressed not in ["None","up","left","right"]:
			lastPressed = "None"
			time.sleep(sleepTime)
			stopAll()
			
		flushLoop()
			
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	stopAll()
