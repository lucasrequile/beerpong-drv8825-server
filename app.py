from time import sleep
import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, request

DIR1 = 20 #direction GPIO pin 1 | pin 13
STEP1 = 21 #Step GPIO pin 1 | pin 11
DIR2 = 24 #direction GPIO pin 2 | pin 18
STEP2 = 23 #Step GPIO pin 2 | pin 16
DIR3 = 8 #direction GPIO pin 3 | pin 24 
STEP3 = 25 #Step GPIO pin 3| pin 22 
DIR4 = -1 #direction GPIO pin 4 | pin -1 
STEP4 = -1 #Step GPIO pin 4| pin -1
CW = 1 #clockwise rotation
CCW = 0 #counterclockwise rotation
SPR = 200 #steps per rotation: 1.8/360
millimeter1 = 300
millimeter3 = 10
millimeter4 = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.setup(DIR3, GPIO.OUT)
GPIO.setup(STEP3, GPIO.OUT)
GPIO.output(DIR1, CW)
GPIO.output(DIR2, CW)
GPIO.output(DIR3, CW)

MODE1 = (13,20,21) #(3,5,7)
MODE2 = (14,15,18) #(8,10,12)
MODE3 = (2,3,4) #(36,38,40)

GPIO.setup(MODE1, GPIO.OUT)
GPIO.setup(MODE2, GPIO.OUT)
GPIO.setup(MODE3, GPIO.OUT)

RESOLUTION = {
	'Full': (0,0,0),
	'Half': (1,0,0),
	'1/4': (0,1,0),
	'1/8': (1,1,0),
	'1/16': (0,0,1),
	'1/32': (1,0,1)
}

step_count = SPR * 2
delay = 1/step_count

def moveOneMotor(MODE,DIR,STEP,rotations,direction):
    GPIO.output(MODE, RESOLUTION['Half'])
    step_count = int(SPR * rotations *2)
    delay = .0005/2
    GPIO.output(DIR, direction)
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    print("turn completed")

def moveTwoMotors(MODEA, MODEB, DIRA, DIRB, STEPA, STEPB, rotations, direction):
    GPIO.output(MODEA, RESOLUTION['Half'])
    GPIO.output(MODEB, RESOLUTION['Half'])
    step_count = int(SPR * rotations *2)
    delay = .0005/2
    GPIO.output(DIRA, direction)
    GPIO.output(DIRB, direction)
    for x in range(step_count):
        GPIO.output(STEPA, GPIO.HIGH)
        GPIO.output(STEPB, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEPA, GPIO.LOW)
        GPIO.output(STEPB, GPIO.LOW)
        sleep(delay)
    print("movement completed")

app = Flask(__name__, static_url_path='/static')
@app.route('/')
def home():
    return render_template("index.html", dirpin1 = DIR1, 
        dirpin2 = DIR2,
        dirpin3 = DIR3,
        dirpin4 = DIR4,
        steppin1 = STEP1,
        steppin2 = STEP2,
        steppin3 = STEP3,
        steppin4 = STEP4,
        millimeter1 = millimeter1,
        millimeter3 = millimeter3,
        millimeter4 = millimeter4)

@app.route("/move_motor_1and2")
def move_motor1and2():
    direction = CW
    moveTwoMotors(MODE1, MODE2, DIR1, DIR2, STEP1, STEP2, millimeter1/2, direction)
    return f'motor 1 + 2 moved {millimeter1} mm in direction {direction}'

@app.route("/move_motor3")
def move_motor3():
    direction = CW
    moveOneMotor(MODE3, DIR3, STEP3, millimeter3/2, direction)
    return f'motor 3 moved {millimeter3} mm in direction {direction}'

@app.route("/move_motor4")
def move_motor4():
    direction = CW
    moveOneMotor(MODE4, DIR4, STEP4, millimeter4/2, direction)
    return f'motor 4 moved {millimeter4} mm in direction {direction}'


@app.route('/customMotor12', methods=['POST'])
def customMotor12():
    input_value1 = request.json['input']
    direction = int(request.json['direction'])
    moveTwoMotors(MODE1, MODE2, DIR1, DIR2, STEP1, STEP2, float(input_value1), direction)
    return f'Motor 1 & 2 moved {input_value1} rotations in direction {direction}'

@app.route('/customMotor3', methods=['POST'])
def customMotor3():
    input_value1 = request.json['input']
    direction = request.json['direction']
    moveOneMotor(MODE3, DIR3, STEP3, float(input_value1), direction)
    return f'Motor 3 moved {input_value1} rotations in direction {direction}'

@app.route('/customMotor4', methods=['POST'])
def customMotor4():
    input_value1 = request.json['input']
    direction = int(request.json['direction'])
    moveOneMotor(MODE4, DIR4, STEP4, float(input_value1), direction)
    return f'Motor 4 moved {input_value1} rotations in direction {direction}'

@app.route('/reboot')
def reboot():
    os.system('sudo reboot')
    return 'Rebooting...'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')