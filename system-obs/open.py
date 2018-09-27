#!/usr/bin/python
#
# Open shutter script for INDI Dome Scripting Gateway
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#

import sys
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

coordinates = open('/tmp/indi-status', 'r')
str = coordinates.readline()
coordinates.close()

GPIO.output(17, GPIO.HIGH)
while (GPIO.input(24)):
  sleep(1)
GPIO.output(17, GPIO.LOW)

str = str[0] + ' 1 ' + str[4:]
coordinates = open('/tmp/indi-status', 'w')
coordinates.truncate()
coordinates.write(str)
coordinates.close()

sys.exit(0)

