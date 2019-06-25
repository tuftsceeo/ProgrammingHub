# Example Script for Lesson

## Section 1 - Import packages & define inputs/outputs
import ev3dev.ev3 as ev3
from time import sleep

us = ev3.UltrasonicSensor() # Connect ultrasonic sensor to any sensor port
us.mode='US-DIST-CM' # Put the US sensor into distance mode.
units = us.units # reports 'cm' even though the sensor measures 'mm'

# Define motor outputs
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')
speed = 25 # Set Speed

## Section 2 - Define functions to get the distance, drive the robot, & set LED colors
# Get distance from Ultrasonic Sensor
def getDist():
    return us.value()/10  # convert mm to cm

# Motor commands
def forward():
   motor_left.run_direct(duty_cycle_sp=speed)
   motor_right.run_direct(duty_cycle_sp=speed)

def back():
   motor_left.run_direct(duty_cycle_sp=-speed)
   motor_right.run_direct(duty_cycle_sp=-speed)

def left():
   motor_left.run_direct( duty_cycle_sp=-speed)
   motor_right.run_direct( duty_cycle_sp=speed)

def right():
   motor_left.run_direct( duty_cycle_sp=speed)
   motor_right.run_direct( duty_cycle_sp=-speed)

def stop():
   motor_left.run_direct( duty_cycle_sp=0)
   motor_right.run_direct( duty_cycle_sp=-0)

# LED commands
def red():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)

def yellow():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)

def green():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

## Section 3 - Define functions Drive the EV3 based on user inputs and set the EV3 LED color based on proximity to obstruction

def driveEV3(char): # Drive the EV3 based on user inputs
    if char == 'w':
        forward()
        direc = 'Forward'
    elif char == 's':
        back()
        direc = 'Backward'
    elif char == 'd':
        right()
        direc = 'Right'
    elif char == 'a':
        left()
        direc = 'Left'
    elif char == ' ':
        stop()
        direc = 'Stopped'
    try: print('Direction: %s' % (direc))
    except NameError: print('invalid character')

def setLED(dist): # set the EV3 LED color based on proximity to obstruction
    if dist > 50:
    	green()
    elif dist <= 50 and dist >= 10:
    	yellow()
    elif dist < 10:
    	red()
    print('Distance to Obstruction: %s' % (dist))

# Section 4 - Run the Code until the user presses the "q" key
char = ""
# Operating Instructions
instructions = """---------------------
 KEY         COMMAND
---------------------
 w           Forward
 s           Backward
 a           Left
 d           Right
 space       Stop
 other key   Quit"""
print(instructions)
while True:
    try:
        char = input() # wait for keyboard input
        if char != 'q':
            driveEV3(char)
            dist = getDist()
            setLED(dist)
        else:
            stop()
            print('Quitting')
            raise Exception('quit')
    except Exception:
        break

