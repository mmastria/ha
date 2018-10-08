#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#import sys
#import os
#from gevent import monkey; monkey.patch_all()
#from bottle import route, run

from aiohttp import web
import RPi.GPIO as GPIO
import logging
import logging.handlers
from time import sleep

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


## --------------------------


async def asleep():  
  print('SLEEP', datetime.now())
  time.sleep(1)

def _move():
  log.debug('move')
  if _can_move():
    if _is_moving():
      GPIO.output(ror_move, GPIO.LOW)
      await asleep()
    GPIO.output(ror_move, GPIO.HIGH)
    return True
  return False

def _stop():
  log.debug('stop')
  if _is_moving():
    GPIO.output(ror_move, GPIO.LOW)
    await asleep()
  if _can_stop():
    GPIO.output(ror_move, GPIO.HIGH)
    await asleep()
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
      await asleep()
    while _is_not_open() and _is_moving():
      sleep()
      if _is_closed():
        _move()
        while _is_closed() and _is_moving():
          await asleep()
    if _is_moving():
      GPIO.output(ror_move, GPIO.LOW)
    return True
  return False

def _close():
  log.debug('close')
  if _can_close():
    _move()
    while _is_open():
      await asleep()
    while _is_not_closed() and _is_moving():
      await asleep()
      if _is_open():
        _move()
        while _is_open() and _is_moving():
          await asleep()
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


async def index(request):
  return web.Response(text='REST Services - Roll-Off Roof Controller')

async def can_park(request):
  return web.Response(text='0' if _is_not_closed() or _can_park() else '1')

async def park(request):
  return web.Response(text='0' if _park() else '1')

async def unpark(request):
  return web.Response(text='0' if _unpark() else '1')

async def can_open(request):
  return web.Response(text='0' if _can_open() else '1')

async def open(request):
  return web.Response(text='0' if _open() else '1')

async def can_close(request):
  return web.Response(text='0' if _can_close() else '1')

async def close(request):
  return web.Response(text='0' if _close() else '1')

async def abort(request):
  return web.Response(text='0' if _abort() else '1')

async def status(request):
  return web.Response(text=_status())


## --------------------------


if __name__ == "__main__":
  log.debug("starting roll-off roof manager")
  app = web.Application()
  app.router.add_get('/', index)
  app.router.add_get('/park', can_park)
  app.router.add_put('/park', park)
  app.router.add_put('/unpark', unpark)
  app.router.add_get('/open', can_open)
  app.router.add_put('/open', open)
  app.router.add_get('/close', can_close)
  app.router.add_put('/close', close)
  app.router.add_put('/abort', abort)
  app.router.add_get('/status', status)
  web.run_app(app, port=80)

