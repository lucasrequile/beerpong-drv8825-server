from time import sleep
import RPi.GPIO as GPIO

DIR = 20 #direction GPIO pin 1
STEP = 21 #Step GPIO pin 1
CW = 1 #clockwise rotation
CCW = 0 #counterclockwise rotation
SPR = 200 #steps per rotation: 360/1.8

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

step_count = SPR
delay = 1/SPR

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

sleep(.5)
GPIO.output(DIR, CCW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()
