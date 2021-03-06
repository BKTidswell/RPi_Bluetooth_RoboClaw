<<<<<<< HEAD
import time, threading
=======
import time #, threading
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import neopixel
import board

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

#NeoPixel Setup
pixel_pin = board.D12
num_pixels = 12
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5,auto_write=False, pixel_order=ORDER)
num_pixels = 12

#NeoPixel Pins
pinSections = [[0,1,2,3],[4,5,6,7],[8,9,10,11]]

#neoPixel Colors
RED = (0,255,0)
YELLOW = (255,255,0)
GREEN = (255,0,0)
BLUE = (0,0,255)

colorSets = [[RED,YELLOW,YELLOW],[BLUE,GREEN,GREEN]]
cDir = 0

#sets up motor driver pins
GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
numMotors = 3
IN1PINS = [24,18,11] #[18,12,23] #[8,12,18]
IN2PINS = [25,23,7]  #[22,16,26] #[10,16,22]

#Makes the PMW references
IN1PWMS = [None for x in range(numMotors)]
IN2PWMS = [None for x in range(numMotors)]

#Starts all PWM at 0
for i in range(numMotors):
	pin = IN1PINS[i]
	GPIO.setup(pin,GPIO.OUT)
<<<<<<< HEAD
	IN1PWMS[i] = GPIO.PWM(pin,10000)
=======
	IN1PWMS[i] = GPIO.PWM(pin,100)
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
	IN1PWMS[i].start(0)
	
for i in range(numMotors):
	pin = IN2PINS[i]
	GPIO.setup(pin,GPIO.OUT)
<<<<<<< HEAD
	IN2PWMS[i] = GPIO.PWM(pin,10000)
=======
	IN2PWMS[i] = GPIO.PWM(pin,100)
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
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

<<<<<<< HEAD
motorTop = 0.8

#creates motor winding functions
def motorControl(mNum,speed):
	if speed*MDirs[mNum] >= 0:
		IN1PWMS[mNum].ChangeDutyCycle(int(speed*spdMax*MDirs[mNum]*motorTop))
		IN2PWMS[mNum].ChangeDutyCycle(0)
	else:
		IN1PWMS[mNum].ChangeDutyCycle(0)
		IN2PWMS[mNum].ChangeDutyCycle(int(abs(speed*spdMax*MDirs[mNum]*motorTop)))
=======
#creates motor winding functions
def motorControl(mNum,speed):
	if speed*MDirs[mNum] >= 0:
		IN1PWMS[mNum].ChangeDutyCycle(int(speed*spdMax*MDirs[mNum]))
		IN2PWMS[mNum].ChangeDutyCycle(0)
	else:
		IN1PWMS[mNum].ChangeDutyCycle(0)
		IN2PWMS[mNum].ChangeDutyCycle(int(abs(speed*spdMax*MDirs[mNum])))
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d

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

def light_all(r,g,b):
	pixels.fill((r,g,b))
	pixels.show()

def pixelSections(sections,colors):
	for i in range(3):
		s = sections[i]
		for j in pinSections[s]:
			pixels[j] = (colors[i])
	pixels.show()

#creates object 'gamepad' to store the data
gamepadConnect = False
while(not gamepadConnect):
	light_all(255,0,0)
	try:
		gamepad = InputDevice('/dev/input/event0')
		gamepadConnect = True
		#prints out device info at start
		print(gamepad)
		#Change Light Color
		pixelSections([topM,rightM,leftM],colorSets[cDir])
	except:
		print("No Gamepad Connected. Please turn it on!")
		light_all(255,255,0)
		time.sleep(0.5)

<<<<<<< HEAD
#t = threading.Timer(0.01,stopAll)
#t.start()

=======
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
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
						pixelSections([topM,rightM,leftM],colorSets[cDir])
						allowRotate = False
					print("Left Trigger")
				elif event.code == rTrig:
					#Rotate Contact Right (Clock)
					if allowRotate:
						(topM,rightM,leftM) = rotateRight(topM,rightM,leftM)
						pixelSections([topM,rightM,leftM],colorSets[cDir])
						allowRotate = False
					print("Right Trigger")
				elif event.code == yBtn:
					#Turn Left
<<<<<<< HEAD
					runMotorPattern([rightM,leftM,leftM,rightM,rightM,leftM],[1,1,0,0,-1,-1],[2,2,0,0.1,0.666,1.333])
=======
					runMotorPattern([rightM,leftM,rightM,leftM],[1,1,-1,-1],[3,3,1,2])
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
					(topM,rightM,leftM) = rotateRight(topM,rightM,leftM)
					pixelSections([topM,rightM,leftM],colorSets[cDir])
					print("Y")
					lastPressed = "Y"
				elif event.code == xBtn:
					#Turn Right
<<<<<<< HEAD
					runMotorPattern([leftM,rightM,leftM,rightM,leftM,rightM],[1,1,0,0,-1,-1],[2,2,0,0.1,0.666,1.333])
=======
					runMotorPattern([leftM,rightM,leftM,rightM],[1,1,-1,-1],[3,3,1,2])
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
					(topM,rightM,leftM) = rotateLeft(topM,rightM,leftM)
					pixelSections([topM,rightM,leftM],colorSets[cDir])
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
<<<<<<< HEAD
						runMotorPattern([topM,rightM,leftM],[1,1,1],[0,0,1.5])
					else:
						runMotorPattern([topM,rightM,leftM],[-1,-1,-1],[0,0,1])
=======
						runMotorPattern([topM,rightM,leftM],[1,1,1],[0,0,1])
					else:
						runMotorPattern([topM,rightM,leftM],[-1,-1,-1],[0,0,0.75])
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
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
<<<<<<< HEAD
					#t = threading.Timer(tTime,stopAll)
					#t.start()
=======
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
					lastPressed = "up"
					print("Up")
				elif event.value == down:
					revRun = not revRun
					if revRun:
						cDir = 1
						print("Motors Unwinding")
					else:
						cDir = 0
						print("Motors Winding")
					pixelSections([topM,rightM,leftM],colorSets[cDir])
				elif event.value == middle:
					stopAll()
<<<<<<< HEAD
					#t.cancel()
=======
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
			elif event.code == x:	
				if event.value == left:
					#Move Left
					if not revRun:
						motorControl(leftM,1)
					else:
						motorControl(leftM,-1)
<<<<<<< HEAD
					#t = threading.Timer(tTime,stopAll)
					#t.start()
=======
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
					lastPressed = "left"
					print("Left")
				elif event.value == right:
					#Move Right
					if not revRun:
						motorControl(rightM,1)
					else:
						motorControl(rightM,-1)
<<<<<<< HEAD
					#t = threading.Timer(tTime,stopAll)
					#t.start()
=======
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
					lastPressed = "right"
					print("Right")
				elif event.value == middle:
					stopAll()
<<<<<<< HEAD
					#t.cancel()
=======
>>>>>>> f6ecfeb29db0c993fbd7d465a202a3283db2c36d
		
		if lastPressed not in ["None","up","left","right"]:
			lastPressed = "None"
			time.sleep(sleepTime)
			stopAll()
			
		flushLoop()
			
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	stopAll()
