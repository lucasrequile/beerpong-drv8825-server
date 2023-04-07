from time import sleep
import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, request

DIR1 = 14 #direction GPIO pin 1 | pin 13
STEP1 = 15 #Step GPIO pin 1 | pin 11
EN1 = 18
DIR2 = 23 #direction GPIO pin 2 | pin 18
STEP2 = 24 #Step GPIO pin 2 | pin 16
EN2 = 25
DIR3 = 17 #direction GPIO pin 3 | pin 24 
STEP3 = 27 #Step GPIO pin 3| pin 22 
EN3 = 22
DIR4 = 10 #direction GPIO pin 4 | pin -1 
STEP4 = 9 #Step GPIO pin 4| pin -1
EN4 = 11
CW = 1 #clockwise rotation
CCW = 0 #counterclockwise rotation
SPR = 200 #steps per rotation: 1.8/360
millimeter1 = 300
millimeter3 = 10
millimeter4 = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)
GPIO.setup(EN1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.setup(EN2, GPIO.OUT)
GPIO.setup(DIR3, GPIO.OUT)
GPIO.setup(STEP3, GPIO.OUT)
GPIO.setup(EN3, GPIO.OUT)
GPIO.setup(DIR4, GPIO.OUT)
GPIO.setup(STEP4, GPIO.OUT)
GPIO.setup(EN4, GPIO.OUT)
GPIO.output(DIR1, CW)
GPIO.output(DIR2, CW)
GPIO.output(DIR3, CW)
GPIO.output(DIR4, CW)

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

def moveOneMotor(DIR,STEP,rotations,direction):
    step_count = int(SPR * rotations *2)
    delay = .0005/2
    GPIO.output(DIR, direction)
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    print("turn completed")

def moveTwoMotors(DIRA, DIRB, STEPA, STEPB, rotations, direction):
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
    return render_template("index.html", \
        dirpin1 = DIR1, 
        dirpin2 = DIR2,
        dirpin3 = DIR3,
        dirpin4 = DIR4,
        steppin1 = STEP1,
        steppin2 = STEP2,
        steppin3 = STEP3,
        steppin4 = STEP4,
        enpin1 = EN1,
        enpin2 = EN2,
        enpin3 = EN3,
        enpin4 = EN4,
        millimeter1 = millimeter1,
        millimeter3 = millimeter3,
        millimeter4 = millimeter4)

@app.route("/move_motor_1and2")
def move_motor1and2():
    direction = CW
    moveTwoMotors(DIR1, DIR2, STEP1, STEP2, millimeter1/2, direction)
    return f'motor 1 + 2 moved {millimeter1} mm in direction {direction}'

@app.route("/move_motor3")
def move_motor3():
    direction = CW
    moveOneMotor(DIR3, STEP3, millimeter3/2, direction)
    return f'motor 3 moved {millimeter3} mm in direction {direction}'

@app.route("/move_motor4")
def move_motor4():
    direction = CW
    moveOneMotor(DIR4, STEP4, millimeter4/2, direction)
    return f'motor 4 moved {millimeter4} mm in direction {direction}'

@app.route('/customMotor12', methods=['POST'])
def customMotor12():
    input_value1 = request.json['input']
    direction = int(request.json['direction'])
    moveTwoMotors(DIR1, DIR2, STEP1, STEP2, float(input_value1), direction)
    return f'Motor 1 & 2 moved {input_value1} rotations in direction {direction}'

@app.route('/customMotor3', methods=['POST'])
def customMotor3():
    input_value1 = request.json['input']
    direction = request.json['direction']
    moveOneMotor(DIR3, STEP3, float(input_value1), direction)
    return f'Motor 3 moved {input_value1} rotations in direction {direction}'

@app.route('/customMotor4', methods=['POST'])
def customMotor4():
    input_value1 = request.json['input']
    direction = int(request.json['direction'])
    moveOneMotor(DIR4, STEP4, float(input_value1), direction)
    return f'Motor 4 moved {input_value1} rotations in direction {direction}'

@app.route("/disableAll")
def disableAll():
    GPIO.output(EN1, GPIO.HIGH)
    GPIO.output(EN2, GPIO.HIGH)
    GPIO.output(EN3, GPIO.HIGH)
    GPIO.output(EN4, GPIO.HIGH)
    return 'All motors disabled'

@app.route("/disable1")
def disable1():
    GPIO.output(EN1, GPIO.HIGH)
    return 'motor 1 disabled'

@app.route("/disable2")
def disable2():
    GPIO.output(EN2, GPIO.HIGH)
    return 'motor 2 disabled'

@app.route("/disable3")
def disable3():
    GPIO.output(EN3, GPIO.HIGH)
    return 'motor 3 disabled'

@app.route("/disable4")
def disable4():
    GPIO.output(EN4, GPIO.HIGH)
    return 'motor 4 disabled'

@app.route("/enableAll")
def enableAll():
    GPIO.output(EN1, GPIO.LOW)
    GPIO.output(EN2, GPIO.LOW)
    GPIO.output(EN3, GPIO.LOW)
    GPIO.output(EN4, GPIO.LOW)
    return 'All motors enabled'

@app.route("/enable1")
def enable1():
    GPIO.output(EN1, GPIO.LOW)
    return 'motor 1 enabled'

@app.route("/enable2")
def enable2():
    GPIO.output(EN2, GPIO.LOW)
    return 'motor 2 enabled'

@app.route("/enable3")
def enable3():
    GPIO.output(EN3, GPIO.LOW)
    return 'motor 3 enabled'

@app.route("/enable4")
def enable4():
    GPIO.output(EN4, GPIO.LOW)
    return 'motor 4 enabled'

@app.route('/reboot')
def reboot():
    os.system('sudo shutdown -r 1')
    return 'Rebooting in 1 min...'

@app.route('/rebootImmediately')
def rebootImmediately():
    os.system('sudo shutdown -r now')
    return 'Rebooting...'

@app.route('/shutdown')
def shutdown():
    os.system('sudo shutdown 1')
    return 'Shutting down in 1 min...'

@app.route('/cancelShutdown')
def cancelShutdown():
    os.system('sudo shutdown -c')
    return 'Shutdown canceled'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
