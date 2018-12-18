import time
from roboclaw import Roboclaw

#Windows comport name
#rc = Roboclaw("COM9",115200)
#Linux comport name
rc = Roboclaw("/dev/ttyACM0",9600)

rc.Open()
address = 0x80

rc.ForwardM2(address,127) #full forwards
print "running forward"
time.sleep(3)
rc.ForwardM2(address,0) #stopped
print "stopped"
rc.BackwardM2(address,127) #full back
print "running backwards"
time.sleep(3)
rc.ForwardM2(address,0) #stopped
print "stopped"

rc.ForwardM1(address,64) #half forwards
print "running half forward"
time.sleep(3)
rc.ForwardM1(address,0) #stopped
print "stopped"
rc.BackwardM1(address,64) #half back
print "running half backwards"
time.sleep(3)
rc.ForwardM1(address,0) #stopped
print "stopped"
