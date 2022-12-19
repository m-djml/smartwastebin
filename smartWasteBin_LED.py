# if the bin is full => Red Light
# if the bin is half empty => BLUE Light
# else GREEN Light, the waste bin does need to be collected

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#set the pinout for the utltrasound sensor
TRIG = 23
ECHO = 24

#set the pinout for the Leds
RED = 7
BLUE = 8
GREEN = 25
BUZZER = 27

print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(BUZZER,GPIO.OUT)
Buzz = GPIO.PWM(BUZZER, 440)

try:
    while True:

        GPIO.output(TRIG, False)
        print ("Waiting For Sensor To Settle")
        time.sleep(0.1)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
          pulse_start = time.time()

        while GPIO.input(ECHO)==1:
          pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)

        print ("Distance:",distance,"cm")

        if distance < 25:
            GPIO.output(RED,GPIO.HIGH)
            GPIO.output(BLUE,GPIO.LOW)
            GPIO.output(GREEN,GPIO.LOW)
            print ("waste bin is full")
            Buzz.start(50)
        elif distance < 70:
            Buzz.stop()
            GPIO.output(RED,GPIO.LOW)
            GPIO.output(BLUE,GPIO.HIGH)
            GPIO.output(GREEN,GPIO.LOW)
            print ("waste bin is half full")
        else:
            Buzz.stop()
            GPIO.output(RED,GPIO.LOW)
            GPIO.output(BLUE,GPIO.LOW)
            GPIO.output(GREEN,GPIO.HIGH)
            print ("waste bin does not need to be collected")

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    GPIO.cleanup()
