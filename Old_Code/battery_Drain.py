import time
from roboclaw import Roboclaw
from evdev import InputDevice, categorize, ecodes
import datetime

#Opens up roboclaw inputs

rc1 = Roboclaw("/dev/ttyACM1",9600)
rc2 = Roboclaw("/dev/ttyACM0",9600)

rc1.Open()
rc2.Open()

address = 0x80

#defines full speed
spdMax = 63

#defines motor positions
topM = 2
rightM = 1
leftM = 3

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

while(True):
    motorControl(1,1)
    motorControl(2,1)
    motorControl(3,1)

    timeStr = str(datetime.datetime.now())+"\n"
    text_file = open("Output.txt","a")
    text_file.write(timeStr)
    text_file.close()

    time.sleep(1)
    stopAll()
    time.sleep(1)
