from time import sleep
import RPi.GPIO as GPIO

DIR1 = 27 #direction GPIO pin 1 | pin 13
STEP1 = 17 #Step GPIO pin 1 | pin 11
DIR2 = 24 #direction GPIO pin 2 | pin 18
STEP2 = 23 #Step GPIO pin 2 | pin 16
DIR3 = 8 #direction GPIO pin 3 | pin 24 
STEP3 = 25 #Step GPIO pin 3| pin 22 
CW = 1 #clockwise rotation
CCW = 0 #counterclockwise rotation
SPR = 200 #steps per rotation: 1.8/360

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.output(DIR1, CW)
GPIO.output(DIR2, CW)

MODE1 = (2,3,4) #(3,5,7)
MODE2 = (14,15,18) #(8,10,12)
MODE3 = (16,20,21) #(36,38,40)

GPIO.setup(MODE1, GPIO.OUT)
GPIO.setup(MODE2, GPIO.OUT)
RESOLUTION = {
	'Full': (0,0,0),
	'Half': (1,0,0),
	'1/4': (0,1,0),
	'1/8': (1,1,0),
	'1/16': (0,0,1),
	'1/32': (1,0,1)
}
GPIO.output(MODE1, RESOLUTION['Half'])
GPIO.output(MODE2, RESOLUTION['Half'])

step_count = SPR *2
delay = 1/step_count

for x in range(step_count):
	GPIO.output(STEP1, GPIO.HIGH)
	GPIO.output(STEP2, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP1, GPIO.LOW)
	GPIO.output(STEP2, GPIO.LOW)
	sleep(delay)

sleep(.5)
GPIO.output(DIR1, CCW)
GPIO.output(DIR2, CCW)

for x in range(step_count):
	GPIO.output(STEP1, GPIO.HIGH)
	GPIO.output(STEP2, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP1, GPIO.LOW)
	GPIO.output(STEP2, GPIO.LOW)
	sleep(delay)
