import lib.GPIO_Intel as GPIO
import time, sys, os
Gpio = GPIO.Intel()
Gpio.setup('IO12')
Gpio.output('IO12', '1')
print("done")

