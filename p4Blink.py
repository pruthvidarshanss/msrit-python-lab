"""
PROGRAM 4
------------------------------------------------------------------------------------------------------------------
Write a Python program demonstrate continous blinking of a LED (blinking effect) 
using Raspberry PI and RPi.GPIO library
"""

import RPi.GPIO as GPIO
import time


LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN,GPIO.OUT)


try:
    while True:
        GPIO.output(LED_PIN,GPIO.HIGH)
        time.sleep(1) 
        GPIO.output(LED_PIN,GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
    exit()