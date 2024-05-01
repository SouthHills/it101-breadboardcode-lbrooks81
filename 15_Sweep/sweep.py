# Description : Servo sweep
from gpiozero import AngularServo
import time

correction_offset = 0.0 # define pulse offset of servo
maxPW = (2.5 + correction_offset) / 1000 # define pulse duty cycle for minimum angle of servo
minPW = (0.5 - correction_offset) / 1000 # define pulse duty cycle for maximum angle of servo

SERVO = AngularServo(pin=18, initial_angle=0, min_angle=0, max_angle=180, min_pulse_width=minPW, max_pulse_width=maxPW)
SERVO_DELAY = 0.001 # Delay in milliseconds

def loop():
    global SERVO, SERVO_DELAY
    while True:
        for angle in range(0, 181, 1):   # make servo rotate from 0 to 180 deg
            SERVO.angle = angle
            time.sleep(SERVO_DELAY)
        time.sleep(1)
        for angle in range(180, -1, -1): # make servo rotate from 180 to 0 deg
            SERVO.angle = angle
            time.sleep(SERVO_DELAY)
        time.sleep(1)

def destroy():
    global SERVO
    SERVO.close()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
