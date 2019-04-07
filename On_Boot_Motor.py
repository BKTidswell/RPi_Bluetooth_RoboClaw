#!/usr/bin/python -u

import time
from roboclaw import Roboclaw
from evdev import InputDevice, categorize, ecodes
import fnmatch
import os
from datetime import datetime

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
#	  1
#	/	\
#  3 ___ 2

now = datetime.now()
minute = now.strftime("%M")
outFile  = "/home/pi/Desktop/Output"+minute+".txt"
f = open(outFile,"w")

gamepadConnect = False
while(not gamepadConnect):
	try:
		gamepad = InputDevice('/dev/input/event0')
		gamepadConnect = True
	except:
		f.write("No Gamepad Connected. Please turn it on! \n")
		time.sleep(0.5)

f.close()

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

M1Dir = 1
M2Dir = -1
M3Dir = 1

while(True):
	f = open(outFile,"a")
	try:
		for event in gamepad.read_loop():
			if event.type == ecodes.EV_KEY:
				if event.value == 1:
					if event.code == start:
						#E-Stop
						f.write("start")
					elif event.code == select:
						#Motor Reset?
						f.write("select")
					elif event.code == lTrig:
						#Rotate Contact Left (Counterclock)
						tempM = topM
						topM = leftM
						leftM = rightM
						rightM = tempM
						f.write("left bumper")
					elif event.code == rTrig:
						#Rotate Contact Right (Clock)
						tempM = topM
						topM = rightM
						rightM = leftM
						leftM = tempM
						f.write("right bumper")
					elif event.code == yBtn:
						#Turn Left
						lastPressed = "Y"
						f.write("Y")
					elif event.code == bBtn:
						#Inch
						lastPressed = "B"
						f.write("B")
					elif event.code == aBtn:
						#Crunch
						lastPressed = "A"
						f.write("A")
					elif event.code == xBtn:
						#Turn Right
						lastPressed = "X"
						f.write("X")
						
			if event.value == 0 and event.code in buttonDict.keys() and not constRun:
				if lastPressed == buttonDict[event.code]:
					lastPressed = "None"
					
			elif event.type == ecodes.EV_ABS:	 
				if event.code == y:
					if event.value == up:
						#Lift
						lastPressed = "up"
						f.write("up")
					elif event.value == down:
						f.write("down")
					elif event.value == middle:
						pass
				elif event.code == x:	
					if event.value == left:
						lastPressed = "left"
						f.write("left")
					elif event.value == right:
						lastPressed = "right"
						f.write("right")
					elif event.value == middle:
						pass
					
			if lastPressed not in ["None","up","left","right"]:
				lastPressed = "None"
				
	except KeyboardInterrupt:		   # trap a CTRL+C keyboard interrupt  
		break
		
	finally:
		f.write(":( /n")
		
	f.flush()
	f.close()
	sys.stdout.flush()
	   


