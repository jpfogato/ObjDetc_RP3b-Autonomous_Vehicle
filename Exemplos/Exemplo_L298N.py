# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO
import time

pin16 = 18 #pino fisico 16
pin18 = 16 #pino fisico 16
en = 22 #pino fisico 22
temp1=1

GPIO.setmode(GPIO.BOARD) #define o numero dos pinos como os pinos fisicos do RBR

GPIO.setup(pin16,GPIO.OUT)
GPIO.setup(pin18,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(pin16,GPIO.LOW)
GPIO.output(pin18,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

while(1):

    x=raw_input()

    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(pin16,GPIO.HIGH)
         GPIO.output(pin18,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(pin16,GPIO.LOW)
         GPIO.output(pin18,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(pin16,GPIO.LOW)
        GPIO.output(pin18,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(pin16,GPIO.HIGH)
        GPIO.output(pin18,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(pin16,GPIO.LOW)
        GPIO.output(pin18,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'


    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
