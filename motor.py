#!/usr/bin/env python

# Import required modules
import time
import serial
import RPi.GPIO as GPIO

# Speed and drive control variables
out_pin = 18

# Servo neutral position (home)

try:
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(out_pin,GPIO.OUT)

	servo = GPIO.PWM(out_pin,1000)
	servo.start(100)
	time.sleep(5)

except KeyboardInterrupt:
	print("Keyboard")

finally:
	GPIO.cleanup()
