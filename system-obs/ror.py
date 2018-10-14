#!/usr/bin/python
# -*- coding: UTF-8 -*-

import multiprocessing
import RPi.GPIO as GPIO
from time import sleep
from gevent import monkey
from bottle import route, response, run
import requests
import logging.handlers

monkey.patch_all()

#                 01          marron      3.3v    X -
#                                                 - X     5v  marron                  11
#                                                 - X     GND vermelho                02
# ROR_RL2C        03  (O8)    laranja     GPIO4   X -
#                                               - -
# RLR_RL1C        04  (O7)    amarelo     GPIO17  X X     GPIO18  verde       (O6)    05  ROR_RL1B
# ROR_RL2B        06  (O5)    azul        GPIO27  X
# ROR_RL3B        07  (O4)    vinho       GPIO22  X X     GPIO23  cinza       (O3)    08  ROR_RL4B
#                                                 - X     GPIO24  branco      (O2)    09  ROR_MOVE/2A
# ROR_PARKED/1A   10  (O1)    preto       GPIO10  X -
# ROR_SW4         12  (I4)    vermelho    GPIO09  X X     GPIO25  laranja     (I3)    13  ROR_SWITCH_OPEN
# ROR_SW_CLOSED   14  (I2)    amarelho    GPIO11  X X     GPIO08  verde       (I1)    15  ROR_MOUNT_PARKED

ROR_PARKED = 10
ROR_MOVE = 24
ROR_SW_CLOSED = 11
ROR_SW_OPEN = 25
ROR_MOUNT_PARKED = 8

ROR_RL1B = 18
ROR_RL2B = 27
ROR_RL3B = 22
ROR_RL4B = 23

ROR_RL1C = 17
ROR_RL2C = 04

ROR_SW4 = 9

ROR_AAG_HOST = '192.168.0.205'
ROR_AAG_PORT = 80


class Timer(multiprocessing.Process):
	def __init__(self, interval, function, args=[], kwargs={}):
		super(Timer, self).__init__()
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.finished = multiprocessing.Event()

	def cancel(self):
		"""Stop the timer if it hasn't finished yet"""
		self.finished.set()

	def run(self):
		self.finished.wait(self.interval)
		if not self.finished.is_set():
			self.function(*self.args, **self.kwargs)
		self.finished.set()


class RoR(object):
	# parked        == TRUE  -->  [ Relay Desligado | GPIO.LOW ]
	# sw_close      == TRUE  -->  [ Switch Fechado | FALSE ]
	# mount_parked  == TRUE  -->  [ Switch Fechado | FALSE ]
	# move          == TRUE  -->  [ Relay Ligado | GPIO.HIGH ]
	# 0/1 for unparked/parked, 0/1 for closed/open shutter and azimuth as float.

	log = logging.getLogger(__name__)
	log.setLevel(logging.DEBUG)
	handler = logging.handlers.SysLogHandler(address='/dev/log')
	formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
	handler.setFormatter(formatter)
	log.addHandler(handler)

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ROR_PARKED, GPIO.OUT)
	GPIO.setup(ROR_MOVE, GPIO.OUT)
	GPIO.setup(ROR_SW_CLOSED, GPIO.IN)
	GPIO.setup(ROR_SW_OPEN, GPIO.IN)
	GPIO.setup(ROR_MOUNT_PARKED, GPIO.IN)

	GPIO.setup(ROR_RL1B, GPIO.OUT)
	GPIO.setup(ROR_RL2B, GPIO.OUT)
	GPIO.setup(ROR_RL3B, GPIO.OUT)
	GPIO.setup(ROR_RL4B, GPIO.OUT)

	GPIO.setup(ROR_RL1C, GPIO.OUT)
	GPIO.setup(ROR_RL2C, GPIO.OUT)

	GPIO.setup(ROR_SW4, GPIO.IN)

	def __init__(self):
		self._running = True

	def terminate(self):
		self._running = False

	@staticmethod
	def _is_parked():
		if GPIO.input(ROR_PARKED) == GPIO.LOW:
			return True
		return False

	@staticmethod
	def _is_unparked():
		if GPIO.input(ROR_PARKED) == GPIO.HIGH:
			return True
		return False

	@staticmethod
	def is_not_closed():
		if GPIO.input(ROR_SW_CLOSED):
			return True
		return False

	@staticmethod
	def _is_closed():
		if not GPIO.input(ROR_SW_CLOSED):
			return True
		return False

	@staticmethod
	def _is_not_open():
		if GPIO.input(ROR_SW_OPEN):
			return True
		return False

	@staticmethod
	def _is_open():
		if not GPIO.input(ROR_SW_OPEN):
			return True
		return False

	@staticmethod
	def _is_mount_unparked():
		if GPIO.input(ROR_MOUNT_PARKED):
			return True
		return False

	@staticmethod
	def _is_mount_parked():
		if not GPIO.input(ROR_MOUNT_PARKED):
			return True
		return False

	@staticmethod
	def _is_stopped():
		if GPIO.input(ROR_MOVE) == GPIO.LOW:
			return True
		return False

	@staticmethod
	def _is_moving():
		if GPIO.input(ROR_MOVE) == GPIO.HIGH:
			return True
		return False

	@staticmethod
	def can_open():
		return RoR._is_unparked() and RoR._is_not_open() and RoR._is_mount_parked() and RoR.is_safe()

	@staticmethod
	def can_close():
		return RoR._is_unparked() and RoR.is_not_closed() and RoR._is_mount_parked()

	@staticmethod
	def can_park():
		# return RoR._is_unparked() and RoR._is_closed() and RoR._is_not_open()
		return RoR._is_closed() and RoR._is_not_open()

	@staticmethod
	def can_unpark():
		return RoR._is_parked() and RoR._is_mount_parked() and RoR.is_safe()

	@staticmethod
	def _can_move():
		return RoR._is_unparked() and RoR._is_mount_parked()

	@staticmethod
	def _can_stop():
		return RoR.is_not_closed() and RoR._is_not_open()

	@staticmethod
	def is_safe():
		values = {}
		try:
			url = "http://{}:{}/cgi-bin/cgiLastData".format(ROR_AAG_HOST, ROR_AAG_PORT)
			resp = requests.get(url, timeout=5)
			try:
				for sensor, value in [(pair.split("=")) for pair in resp.text.splitlines()]:
					values[sensor] = value
				if values['safe'] == '0':
					return False
				else:
					return True
			except:
				return False
		except requests.exceptions.ConnectionError:
			return False

	def _move(self):
		self.log.debug('move')
		if self._can_move():
			if self._is_moving():
				GPIO.output(ROR_MOVE, GPIO.LOW)
				sleep(1)
			GPIO.output(ROR_MOVE, GPIO.HIGH)
			return True
		return False

	def _stop(self):
		self.log.debug('stop')
		if self._is_moving():
			GPIO.output(ROR_MOVE, GPIO.LOW)
			sleep(1)
		if self._can_stop():
			GPIO.output(ROR_MOVE, GPIO.HIGH)
			sleep(1)
			GPIO.output(ROR_MOVE, GPIO.LOW)
		return True

	def park(self):
		self.log.debug('park')
		if self.is_not_closed():
			if not self.close():
				return False
		if self.can_park():
			GPIO.output(ROR_PARKED, GPIO.LOW)
			return True
		return False

	def unpark(self):
		self.log.debug('unpark')
		if self.can_unpark() and self.is_safe():
			GPIO.output(ROR_PARKED, GPIO.HIGH)
			return True
		return False

	def open(self):
		self.log.debug('open')
		if self.can_open() and self.is_safe():
			self._move()
			while self._is_closed():
				sleep(1)
			while self._is_not_open() and self._is_moving():
				sleep(1)
				if self._is_closed():
					self._move()
					while self._is_closed() and self._is_moving():
						sleep(1)
			if self._is_moving():
				GPIO.output(ROR_MOVE, GPIO.LOW)
			return True
		return False

	def close(self):
		self.log.debug('close')
		if self.can_close():
			self._move()
			while self._is_open():
				sleep(1)
			while self.is_not_closed() and self._is_moving():
				sleep(1)
				if self._is_open():
					self._move()
					while self._is_open() and self._is_moving():
						sleep(1)
			if self._is_moving():
				GPIO.output(ROR_MOVE, GPIO.LOW)
			return True
		return False

	def abort(self):
		self.log.debug('abort')
		return self._stop()

	# 0/1 for unparked/parked, 0/1 for closed/open shutter and azimuth as float.
	@property
	def status(self):
		p = '1' if self._is_parked() else '0'
		s = '1' if self._is_open() else '0' if self._is_closed() else '-'
		self.log.debug('-- parked:%s / open:%s / closed:%s / mount_parked:%s / safe:%s / file: %s %s 0 ' % (
			self._is_parked(), self._is_open(), self._is_closed(), self._is_mount_parked(), self.is_safe(), p, s))
		return '%s %s 0' % (p, s)

	# --------------------------

	@staticmethod
	def is_sw4_closed():
		if GPIO.input(ROR_SW4) == GPIO.LOW:
			return True
		return False

	@staticmethod
	def is_sw4_open():
		if GPIO.input(ROR_SW4) == GPIO.HIGH:
			return True
		return False

	# --------------------------

	@staticmethod
	def rl1b_is_not_open():
		if GPIO.input(ROR_RL1B):
			return True
		return False

	@staticmethod
	def rl1b_is_not_closed():
		if not GPIO.input(ROR_RL1B):
			return True
		return False

	def rl1b_close(self):
		self.log.debug('rl1b_close')
		if self.rl1b_is_not_closed():
			GPIO.output(ROR_RL1B, GPIO.HIGH)
			return True
		return False

	def rl1b_open(self):
		self.log.debug('rl1b_open')
		if self.rl1b_is_not_open():
			GPIO.output(ROR_RL1B, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def rl2b_is_not_open():
		if GPIO.input(ROR_RL2B):
			return True
		return False

	@staticmethod
	def rl2b_is_not_closed():
		if not GPIO.input(ROR_RL2B):
			return True
		return False

	def rl2b_close(self):
		self.log.debug('rl2b_close')
		if self.rl2b_is_not_closed():
			GPIO.output(ROR_RL2B, GPIO.HIGH)
			return True
		return False

	def rl2b_open(self):
		self.log.debug('rl2b_open')
		if self.rl2b_is_not_open():
			GPIO.output(ROR_RL2B, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def rl3b_is_not_open():
		if GPIO.input(ROR_RL3B):
			return True
		return False

	@staticmethod
	def rl3b_is_not_closed():
		if not GPIO.input(ROR_RL3B):
			return True
		return False

	def rl3b_close(self):
		self.log.debug('rl3b_close')
		if self.rl3b_is_not_closed():
			GPIO.output(ROR_RL3B, GPIO.HIGH)
			return True
		return False

	def rl3b_open(self):
		self.log.debug('rl3b_open')
		if self.rl3b_is_not_open():
			GPIO.output(ROR_RL3B, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def rl4b_is_not_open():
		if GPIO.input(ROR_RL4B):
			return True
		return False

	@staticmethod
	def rl4b_is_not_closed():
		if not GPIO.input(ROR_RL4B):
			return True
		return False

	def rl4b_close(self):
		self.log.debug('rl4b_close')
		if self.rl4b_is_not_closed():
			GPIO.output(ROR_RL4B, GPIO.HIGH)
			return True
		return False

	def rl4b_open(self):
		self.log.debug('rl4b_open')
		if self.rl4b_is_not_open():
			GPIO.output(ROR_RL4B, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def rl1c_is_not_open():
		if GPIO.input(ROR_RL1C):
			return True
		return False

	@staticmethod
	def rl1c_is_not_closed():
		if not GPIO.input(ROR_RL1C):
			return True
		return False

	def rl1c_close(self):
		self.log.debug('rl1c_close')
		if self.rl1c_is_not_closed():
			GPIO.output(ROR_RL1C, GPIO.HIGH)
			return True
		return False

	def rl1c_open(self):
		self.log.debug('rl1c_open')
		if self.rl1c_is_not_open():
			GPIO.output(ROR_RL1C, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def rl2c_is_not_open():
		if GPIO.input(ROR_RL2C):
			return True
		return False

	@staticmethod
	def rl2c_is_not_closed():
		if not GPIO.input(ROR_RL2C):
			return True
		return False

	def rl2c_close(self):
		self.log.debug('rl2c_close')
		if self.rl2c_is_not_closed():
			GPIO.output(ROR_RL2C, GPIO.HIGH)
			return True
		return False

	def rl2c_open(self):
		self.log.debug('rl2c_open')
		if self.rl2c_is_not_open():
			GPIO.output(ROR_RL2C, GPIO.LOW)
			return True
		return False


# --------------------------

# 200 OK
# 202 ACCEPTED
# 409 CONFLICT 


@route('/', method='GET')
def index():
	response.content_type = 'text/html'
	response.status = 200
	return "REST Services - Roll-Off Roof Manager"


@route('/park', method='GET')
def can_park():
	# response.status = 200 if RoR.is_not_closed() or RoR.can_park() else 409
	response.status = 200
	return


@route('/park', method='PUT')
def park():
	ror = RoR()
	p = multiprocessing.Process(target=ror.park)
	p.start()
	response.status = 202
	return


@route('/unpark', method='GET')
def can_unpark():
	response.status = 200 if RoR.can_unpark() else 409
	return


@route('/unpark', method='PUT')
def unpark():
	ror = RoR()
	p = multiprocessing.Process(target=ror.unpark)
	p.start()
	response.status = 202
	return


@route('/open', method='GET')
def can_open():
	response.status = 200 if RoR.can_open() else 409
	return


@route('/open', method='PUT')
def open():
	ror = RoR()
	p = multiprocessing.Process(target=ror.open)
	p.start()
	response.status = 202
	return


@route('/close', method='GET')
def can_close():
	response.status = 200 if RoR.can_close() else 409
	return


@route('/close', method='PUT')
def close():
	ror = RoR()
	p = multiprocessing.Process(target=ror.close)
	p.start()
	response.status = 202
	return


@route('/abort', method='PUT')
def abort():
	ror = RoR()
	p = multiprocessing.Process(target=ror.abort)
	response.status = 202
	p.start()
	return


@route('/status', method='GET')
def status():
	ror = RoR()
	response.content_type = 'text/html'
	response.status = 200
	return ror.status


@route('/safe', method='GET')
def is_safe():
	response.status = 200 if RoR.is_safe() else 409
	return

# --------------------------


@route('/sw4', method='GET')
def sw4_open():
	response.status = 200 if RoR.is_sw4_open() else 409
	return


@route('/rl1b/close', method='PUT')
def rl1b_close():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl1b_close)
	p.start()
	response.status = 202
	return


@route('/rl1b/open', method='PUT')
def rl1b_open():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl1b_open)
	p.start()
	response.status = 202
	return


@route('/rl2b/close', method='PUT')
def rl2b_close():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl2b_close)
	p.start()
	response.status = 202
	return


@route('/rl2b/open', method='PUT')
def rl2b_open():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl2b_open)
	p.start()
	response.status = 202
	return


@route('/rl3b/close', method='PUT')
def rl3b_close():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl3b_close)
	p.start()
	response.status = 202
	return


@route('/rl3b/open', method='PUT')
def rl3b_open():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl3b_open)
	p.start()
	response.status = 202
	return


@route('/rl4b/close', method='PUT')
def rl4b_close():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl4b_close)
	p.start()
	response.status = 202
	return


@route('/rl4b/open', method='PUT')
def rl4b_open():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl4b_open)
	p.start()
	response.status = 202
	return


@route('/rl1c/close', method='PUT')
def rl1c_close():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl1c_close)
	p.start()
	response.status = 202
	return


@route('/rl1c/open', method='PUT')
def rl1c_open():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl1c_open)
	p.start()
	response.status = 202
	return


@route('/rl2c/close', method='PUT')
def rl2c_close():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl2c_close)
	p.start()
	response.status = 202
	return


@route('/rl2c/open', method='PUT')
def rl2c_open():
	ror = RoR()
	p = multiprocessing.Process(target=ror.rl2c_open)
	p.start()
	response.status = 202
	return


# --------------------------

if __name__ == "__main__":
	# t = Timer(10, rotina para fazer pooling do aagcw)
	# t.run()
	run(host='0.0.0.0', port=80, server='gevent')
