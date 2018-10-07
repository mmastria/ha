#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import RPi.GPIO as GPIO
from time import sleep
from gevent import monkey; monkey.patch_all()
from bottle import route, run
import logging
import logging.handlers

# parked        == TRUE  -->  [ Relay Desligado | GPIO.LOW ]
# sw_close      == TRUE  -->  [ Switch Fechado | FALSE ]
# mount_parked  == TRUE  -->  [ Switch Fechado | FALSE ]
# move          == TRUE  -->  [ Relay Ligado | GPIO.HIGH ]

# 0/1 for unparked/parked, 0/1 for closed/open shutter and azimuth as float.

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

# pwr_east = 17
# pwr_west_27

ror_parked = 22
ror_move = 23
ror_sw_closed = 24
ror_sw_open = 25
ror_mount_parked = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ror_parked, GPIO.OUT)
GPIO.setup(ror_move, GPIO.OUT)
GPIO.setup(ror_sw_closed, GPIO.IN)
GPIO.setup(ror_sw_open, GPIO.IN)
GPIO.setup(ror_mount_parked, GPIO.IN)


## --------------------------

def _is_parked():
  if GPIO.input(ror_parked) == GPIO.LOW:
    return True
  return False

def _is_unparked():
  if GPIO.input(ror_parked) == GPIO.HIGH:
    return True
  return False

def _is_not_closed():
  if GPIO.input(ror_sw_closed):
    return True
  return False

def _is_closed():
  if not GPIO.input(ror_sw_closed):
    return True
  return False

def _is_not_open():
  if GPIO.input(ror_sw_open):
    return True
  return False

def _is_open():
  if not GPIO.input(ror_sw_open):
    return True
  return False

def _is_mount_unparked():
  if GPIO.input(ror_mount_parked):
    return True
  return False

def _is_mount_parked():
  if not GPIO.input(ror_mount_parked):
    return True
  return False

def _is_stopped():
  if GPIO.input(ror_move) == GPIO.LOW:
    return True
  return False

def _is_moving():
  if GPIO.input(ror_move) == GPIO.HIGH:
    return True
  return False

def _can_open():
  return _is_unparked() and _is_not_open() and _is_mount_parked()

def _can_close():
  return _is_unparked() and _is_not_closed() and _is_mount_parked()

def _can_park():
  return _is_unparked() and _is_closed() and _is_not_open()

def _can_unpark():
  return _is_parked() and _is_mount_parked()

def _can_move():
  return _is_unparked() and _is_mount_parked()

def _can_stop():
  return _is_not_closed() and _is_not_open()

def _move():
  log.debug('move')
  if _can_move():
    if _is_moving():
      GPIO.output(ror_move, GPIO.LOW)
      sleep(1)
    GPIO.output(ror_move, GPIO.HIGH)
    return True
  return False

def _stop():
  log.debug('stop')
  if _is_moving():
    GPIO.output(ror_move, GPIO.LOW)
    sleep(1)
  if _can_stop():
    GPIO.output(ror_move, GPIO.HIGH)
    sleep(1)
    GPIO.output(ror_move, GPIO.LOW)
  return True

def _park():
  log.debug('park')
  if _is_not_closed():
    if not _close():
      return False
  if _can_park():
    GPIO.output(ror_parked, GPIO.LOW)
    return True
  return False

def _unpark():
  log.debug('unpark')
  if _can_unpark():
    GPIO.output(ror_parked, GPIO.HIGH)
    return True
  return False

def _open():
  log.debug('open')
  if _can_open():
    _move()
    while _is_closed():
      sleep(1)
    while _is_not_open() and _is_moving():
      sleep(1)
      if _is_closed():
        _move()
        while _is_closed() and _is_moving():
          sleep(1)
    if _is_moving():
      GPIO.output(ror_move, GPIO.LOW)
    return True
  return False

def _close():
  log.debug('close')
  if _can_close():
    _move()
    while _is_open():
      sleep(1)
    while _is_not_closed() and _is_moving():
      sleep(1)
      if _is_open():
        _move()
        while _is_open() and _is_moving():
          sleep(1)
    if _is_moving():
      GPIO.output(ror_move, GPIO.LOW)
    return True
  return False

def _abort():
  log.debug('abort')
  return _stop()

# 0/1 for unparked/parked, 0/1 for closed/open shutter and azimuth as float.
def _status():
  p = '1' if _is_parked() else '0'
  s = '1' if _is_open() else '0' if _is_closed() else '-'
  m = '1' if _is_mount_parked() else '0'
  log.debug('-- parked: %s (p:%s) - open: %s - closed: %s (s:%s) - mount_parked: %s (m:%s)' % ( _is_parked(), p, _is_open(), _is_closed(), s, _is_mount_parked(),  m))
  return '%s %s 0' % (p, s)


## --------------------------


@route('/', method='GET')
def index():
  return "REST Services - Roll-Off Roof Manager"

@route('/park', method='GET')
def can_park():
  return '0' if _is_not_closed() or _can_park() else '1'

@route('/park', method='PUT')
def park():
  _park()
  return

@route('/unpark', method='PUT')
def unpark():
  return '0' if _unpark() else '1'

@route('/open', method='GET')
def can_open():
  return '0' if _can_open() else '1'

@route('/open', method='PUT')
def open():
  _open()
  return

@route('/close', method='GET')
def can_close():
  return '0' if _can_close() else '1'

@route('/close', method='PUT')
def close():
  _close()
  return

@route('/abort', method='PUT')
def abort():
  return '0' if _abort() else '1'

@route('/status', method='GET')
def status():
  return _status()


## --------------------------


if __name__ == "__main__":
  log.debug("starting roll-off roof manager")
  run(host='0.0.0.0', port=80, server='gevent')

