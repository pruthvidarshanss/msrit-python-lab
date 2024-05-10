"""
PROGRAM 5
------------------------------------------------------------------------------------------------------------------
Write a Python program demonstrate single sequence of turning ON the LED for one second and then turning it OFF.
"""

import RPi.GPIO as GPIO
import time


LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN,GPIO.OUT)


GPIO.output(LED_PIN,GPIO.HIGH)
time.sleep(1) 
GPIO.output(LED_PIN,GPIO.LOW)
time.sleep(1)

GPIO.cleanup()