"""
PROGRAM 6
------------------------------------------------------------------------------------------------------------------
Write a Python program to detect the intensity of light in surrounding using a LDR(Light Dependent Resistor) 
and display the LDR Value as output.
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

delayt = .1
value = 0
ldr = 7
led = 11

GPIO.setup(led,GPIO.OUT)
GPIO.output(led,False)

def rc_time(ldr: int) -> int:

    count = 0
    GPIO.setup(ldr,GPIO.OUT)
    GPIO.output(ldr,False)
    time.sleep(delayt)
    GPIO.setup(ldr,GPIO.IN)
    
    while (GPIO.input(ldr) == 0):
        count += 1
    return count

try:
    while True:
        print("LDR Value:")
        value = rc_time(ldr)
        print(value)
        
        if (value <= 10000):
            print("Lights are off")
            GPIO.output(led,False)
        if (value > 10000):
            print("Lights are onn")
            GPIO.output(led, True)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
    exit()
    