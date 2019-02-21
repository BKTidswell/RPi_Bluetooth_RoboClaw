import time
from roboclaw import Roboclaw
from evdev import InputDevice, categorize, ecodes

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

rc1 = Roboclaw("/dev/ttyACM1",9600)
rc2 = Roboclaw("/dev/ttyACM0",9600)

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
topM = 2
rightM = 1
leftM = 3

#Used for hold-to-use motor control
lastPressed = "None"
buttonDict = {yBtn:"Y",aBtn:"A",bBtn:"B",xBtn:"X"}

constRun = True #Will not change
revRun = False
sleepTime = 0.5

topDir = -1
rightDir = -1
leftDir = -1

#creates motor winding functions
#forwards

def motorControl(mNum,speed):
	if mNum == 1:
		rc1.ForwardBackwardM1(address,64+int(speed*spdMax))
	elif mNum == 2:
		rc1.ForwardBackwardM2(address,64+int(speed*spdMax))
	elif mNum == 3:
		rc2.ForwardBackwardM1(address,64+int(speed*spdMax))
	else:
		print("Incorrect Motor Number")

def stopAll():
	motorControl(topM,0)
	motorControl(rightM,0)
	motorControl(leftM,0)

motorsConnect = False

while(not motorsConnect):
	try:
		#Opens up roboclaw inputs
		rc1 = Roboclaw("/dev/ttyACM1",9600)
		rc2 = Roboclaw("/dev/ttyACM0",9600)

		rc1.Open()
		rc2.Open()

        	stopAll()
		motorsConnect = True
	except:
		print("Connect Both Motor Drivers")
		time.sleep(0.5)

try:
	for event in gamepad.read_loop():
		if event.type == ecodes.EV_KEY:
			if event.value == 1:
				if event.code == start:
					#E-Stop
					stopAll()
					#print("start")
				elif event.code == select:
					pass
					#Motor Reset?
					#print("select")
				elif event.code == lTrig:
					#Rotate Contact Left (Counterclock)
					tempM = topM
					topM = leftM
					leftM = rightM
					rightM = tempM
					#print("left bumper")
				elif event.code == rTrig:
					#Rotate Contact Right (Clock)
					tempM = topM
					topM = rightM
					rightM = leftM
					leftM = tempM
					#print("right bumper")
				elif event.code == yBtn:
					#Turn Left
					motorControl(topM,topDir*1)
					time.sleep(sleepTime*3)
					motorControl(leftM,leftDir*1)
					time.sleep(sleepTime*3)
					motorControl(topM,topDir*-1)
					time.sleep(sleepTime*4)
					motorControl(leftM,leftDir*-1)
					time.sleep(sleepTime*4)
					lastPressed = "Y"
					#print("Y")
				elif event.code == bBtn:
					#Inch
					motorControl(topM,topDir*-1)
					motorControl(rightM,rightDir*1)
					motorControl(leftM,leftDir*1)
					time.sleep(sleepTime*7)
					motorControl(topM,topDir*1)
					motorControl(rightM,rightDir*-1)
					motorControl(leftM,leftDir*-1)
					time.sleep(sleepTime*6)
					lastPressed = "B"
					#print("B")
				elif event.code == aBtn:
					pass
					#Unwind
					#motorControl(topM,topDir*0.5)
					#motorControl(rightM,rightDir*0.5)
					#motorControl(leftM,leftDir*0.5)
					#lastPressed = "A"
					#print("A")
				elif event.code == xBtn:
					#Turn Right
					motorControl(topM,topDir*0.5)
					motorControl(rightM,rightDir*-1)
					motorControl(leftM,leftDir*-1)
					lastPressed = "X"
					#print("X")
					
		if event.value == 0 and event.code in buttonDict.keys() and not constRun:
			if lastPressed == buttonDict[event.code]:
				lastPressed = "None"
				stopAll()
				
		elif event.type == ecodes.EV_ABS:    
			if event.code == y:
				if event.value == up:
					#Lift
					if not revRun:
						motorControl(topM,topDir*1)
					else:
						motorControl(topM,topDir*-1)
					lastPressed = "up"
					#print("up")
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
						motorControl(leftM,leftDir*1)
					else:
						motorControl(leftM,leftDir*-1)
					lastPressed = "left"
					#print("left")
				elif event.value == right:
					#Move Right
					if not revRun:
						motorControl(rightM,rightDir*1)
					else:
						motorControl(rightM,rightDir*-1)
					lastPressed = "right"
					#print("right")
				elif event.value == middle:
					stopAll()
		
		if lastPressed not in ["None","up","left","right"]:
			lastPressed = "None"
			time.sleep(sleepTime)
			stopAll()
			


except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	stopAll()
	   


