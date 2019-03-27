import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD 
GPIO.setup(14, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(15, GPIO.OUT)           # set GPIO24 as an output  

p1 = GPIO.PWM(14, 10000)  # Start PWM 
p2 = GPIO.PWM(15, 10000)  # Start PWM 


  
try:  
    while True:
    	p1.start(0)  			#full back
    	p2.start(75)
    	sleep(1)
        #p1.ChangeDutyCycle(0) 
        #p2.ChangeDutyCycle(50)
        #sleep(1)
        #p1.ChangeDutyCycle(0) 
        #p2.ChangeDutyCycle(100)
        #sleep(1)
        #p1.ChangeDutyCycle(50) 
        #p2.ChangeDutyCycle(100)
        #sleep(1)
        #p1.ChangeDutyCycle(100) 
        #p2.ChangeDutyCycle(100)
        #sleep(1)
  
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	p1.stop()
	p2.stop()
	GPIO.cleanup()          