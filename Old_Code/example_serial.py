from roboclaw2 import Roboclaw
from time import sleep

addesses = [0x80, 0x81]
roboclaw = Roboclaw("/dev/ttyS0",38400)
roboclaw.Open()

while True:
	for address in addesses:
		roboclaw.DutyM2(address,32000)
		print("On")
		sleep(1)
		roboclaw.DutyM2(address,16000)
		print("Half")
		sleep(1)
		roboclaw.DutyM2(address,0)
		print("Off")
		sleep(1)

    
