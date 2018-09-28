#!/usr/bin/python

import sys
import RPi.GPIO as GPIO
from time import sleep

import logging
import logging.handlers

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

# log.debug('this is debug')
# log.critical('this is critical')

# pwr_east = 17
# pwr_west_27

ror_parked = 22
ror_pulse = 23
ror_sw_closed = 24
ror_sw_open = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ror_parked, GPIO.OUT)
GPIO.setup(ror_pulse, GPIO.OUT)
GPIO.setup(ror_sw_closed, GPIO.IN)
GPIO.setup(ror_sw_open, GPIO.IN)

def is_parked():
  # ror parked
  if (GPIO.input(ror_parked) == GPIO.LOW):
    return True
  return False

def is_not_parked():
  # ror not parked
  if (GPIO.input(ror_parked) == GPIO.HIGH):
    return True
  return False

def park():
  log.debug('do park')
  if not is_closed and is_not_parked():
    if not close():
      return False
  if is_closed() and is_stopped() and is_not_parked():
    GPIO.output(ror_parked, GPIO.LOW)
    log.debug('do park return True')
    return True
  log.debug('do park return False')
  return False

def unpark():
  if is_closed() and is_stopped() and is_parked():
    GPIO.output(ror_parked, GPIO.HIGH)
    log.debug('do unpark return True')
    return True
  log.debug('do unpark return False')
  return False

def is_open():
  # ror open
  if (not GPIO.input(ror_sw_open)):
    return True
  return False

def is_closed():
  # ror closed
  if (not GPIO.input(ror_sw_closed)):
    return True
  return False

def is_moving():
  if (GPIO.input(ror_pulse) == GPIO.HIGH):
    return True
  return False

def is_stopped():
  if (GPIO.input(ror_pulse) == GPIO.LOW):
    return True
  return False

# 0/1 for unparked/parked, 0/1 for closed/open shutter and azimuth as float.
def status():
  p = '1' if is_parked() else '0'
  s = '1' if is_open() else '0'
  return '%s %s 0' % (p, s)

def can_open():
  # ror not open
  return not is_open() and not is_parked() and not is_moving()

def can_close():
  # ror not closed
  return not is_closed() and is_not_parked() and not is_moving()

def move():
  log.debug('do move')
  if is_not_parked() and not is_moving():
    GPIO.output(ror_pulse, GPIO.LOW)
    sleep(1)
    GPIO.output(ror_pulse, GPIO.HIGH)

def stop():
  log.debug('do stop')
  if is_moving():
    GPIO.output(ror_pulse, GPIO.LOW)
  if not is_open() and not is_closed():
    sleep(1)
    GPIO.output(ror_pulse, GPIO.HIGH)
    sleep(1)
    GPIO.output(ror_pulse, GPIO.LOW)

def open():
  log.debug('do open')
  if can_open():
    log.debug('can open and not is moving')
    move()
    log.debug('move')
    while is_closed():
      log.debug('while is closed')
      sleep(1)
    while (not is_open() and is_moving()):
      log.debug('while not is open and is moving')
      sleep(1)
      if is_closed():
        log.debug('is closed')
        stop()
        log.debug('stop')
        sleep(1)
        move()
        log.debug('move')
        while is_closed() and is_moving():
          log.debug('while is closed')
          sleep(1)
    if is_stopped():
      log.debug('is stopped return false')
      return False
    stop()
    log.debug('stop and return true')
    return True
  log.debug('return false')
  return False

def close():
  log.debug('do close')
  if can_close():
    move()
    while is_open():
      sleep(1)
    while (not is_closed() and is_moving()):
      sleep(1)
      if is_open():
        stop()
        sleep(1)
        move()
        while is_open() and is_moving():
          sleep(1)
    if is_stopped():
      return False
    stop()
    return True
  return False

def abort():
  if is_moving():
    stop()
    return True
  return False


