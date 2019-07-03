import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

numMotors = 4

IN1PINS = [8,12,18,24]
IN2PINS = [10,16,22,26]
SFPINS = [11,15,21,29]
FBPINS = [13,19,23,31]

IN1PWMS = [None for x in range(numMotors)]
IN2PWMS = [None for x in range(numMotors)]

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

for pin in SFPINS:
	GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

for pin in FBPINS:
	GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	
def motorForwards(i):
	IN1PWMS[i].ChangeDutyCycle(100)
	IN2PWMS[i].ChangeDutyCycle(0)
	
def motorBackwards(i):
	IN1PWMS[i].ChangeDutyCycle(0)
	IN2PWMS[i].ChangeDutyCycle(100)

def getSFFlags():
	flags = [GPIO.input(SFPINS[i]) for i in range(numMotors)]
	return(flags)
	
def getFBFlags():
	flags = [GPIO.input(FBPINS[i]) for i in range(numMotors)]
	return(flags)
	
def stopAll():
	for p in IN1PWMS:
		p.ChangeDutyCycle(0)
	for p in IN2PWMS:
		p.ChangeDutyCycle(0)

try:
	while True:
		motorForwards(1)
		print("Forward")
		print(getSFFlags())
		print(getFBFlags())
		time.sleep(2)

		motorBackwards(1)
		print("Back")
		print(getSFFlags())
		print(getFBFlags())
		time.sleep(2)

except KeyboardInterrupt:
	print("Stopped")
	stopAll()
	GPIO.cleanup()
