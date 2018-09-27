#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)


GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)

while (True):

  if GPIO.input(24) == False:
      print('+++ 24 Closed')
  else:
      print('--- 24 Opened')
  if GPIO.input(25) == False:
      print('+++ 25 Closed')
  else:
      print('--- 25 Opened')

  GPIO.output(17, GPIO.HIGH)
  GPIO.output(27, GPIO.HIGH)
  GPIO.output(22, GPIO.HIGH)
  GPIO.output(23, GPIO.HIGH)
  sleep(3)
  GPIO.output(17, GPIO.LOW)
  GPIO.output(27, GPIO.LOW)
  GPIO.output(22, GPIO.LOW)
  GPIO.output(23, GPIO.LOW)
  sleep(3)

