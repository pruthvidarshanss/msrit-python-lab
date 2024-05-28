"""
Program 4
--------------------------------------------------------------------------------------------------------------
Write a Python program to detect the intensity of light in a room using a LDR(Light Dependent Resistor) 
and display the LDR Value as output. If the light is dim , then ON the red LED, else on the Green LED.
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

delay = 0.1
value = 0

ldr = 7
green_led = 11
red_led = 13

GPIO.setup(green_led, GPIO.OUT)
GPIO.output(green_led, False)

GPIO.setup(red_led, GPIO.OUT)
GPIO.output(red_led, False)


def rc_time(ldr):
    count = 0

    GPIO.setup(ldr, GPIO.OUT)
    GPIO.output(ldr, False)
    time.sleep(delay)

    GPIO.setup(ldr, GPIO.IN)

    while GPIO.input(ldr) == 0:
        count += 1
    
    return count


try:
    while True:
        print("LDR value:\t")
        value = rc_time(ldr)
        print(value)

        if value <= 10000:
            print("Lights are ON")
            GPIO.output(red_led, False)
            GPIO.output(green_led, True)
        else:
            print("Lights are OFF")
            GPIO.output(green_led, False)
            GPIO.output(red_led, True)

except KeyboardInterrupt:
    exit()

finally:
    GPIO.cleanup()