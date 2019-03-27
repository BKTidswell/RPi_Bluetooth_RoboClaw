import time
from roboclaw import Roboclaw

#Windows comport name
#rc = Roboclaw("COM9",115200)
#Linux comport name
rc = Roboclaw("/dev/ttyACM0",9600)

rc.Open()
address = 0x80

rc.ForwardBackwardM2(address,64+63) #full forwards
print "running forward"
time.sleep(3)
rc.ForwardBackwardM2(address,64) #stopped
print "stopped"
rc.ForwardBackwardM2(address,64-63) #full back
print "running backwards"
time.sleep(3)
rc.ForwardBackwardM2(address,64) #stopped
print "stopped"

rc.ForwardBackwardM1(address,64+32) #half forwards
print "running half forward"
time.sleep(3)
rc.ForwardBackwardM1(address,64+0) #stopped
print "stopped"
rc.ForwardBackwardM1(address,64-32) #half back
print "running half backwards"
time.sleep(3)
rc.ForwardBackwardM1(address,64+0) #stopped
print "stopped"
