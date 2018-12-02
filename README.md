# RPi_Bluetooth_RoboClaw

This repository has the code used the develop the RoboSoft Catapillar made by Tufts students Ben Tidswell, Jasmine Falk, Alex Bock, Anthony Scibelli, and Cassandra Donatelli. 

The code used for the robot: 
  * bt_control_motors: This is the code the integrates the commands from the bluetooth controllers with the signals to the Roboclaws in order to control the robot
  * roboclaw.py: This is the provided RoboClaw library that we call functions from in order to run the RoboClaws
 
Outdated code:
  * motor.py: an attempt to control the motors with pwm
  * serialMotor.py: a simple example of controlling the RoboClaw with serial commands
  * 8bitdoDemo.py: a simple version of bluetooth control that showed that we had the correct mappings for the 8bitdo bluetooth controller
