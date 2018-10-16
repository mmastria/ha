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
# PWR_RL2C        03  (O8)    laranja     GPIO4   X -
#                                                 - -
# PWR_RL1C        04  (O7)    amarelo     GPIO17  X X     GPIO18  verde       (O6)    05  PWR_RL1B
# PWR_RPI/2B      06  (O5)    azul        GPIO27  X -
# PWR_SCOPE/3B    07  (O4)    vinho       GPIO22  X X     GPIO23  cinza       (O3)    08  PWR_MAIN/4B
#                                                 - X     GPIO24  branco      (O2)    09  ROR_MOVE/2A
# ROR_PARKED/1A   10  (O1)    preto       GPIO10  X -
# ROR_AAGSAFE     12  (I4)    vermelho    GPIO09  X X     GPIO25  laranja     (I3)    13  ROR_SWITCH_OPEN
# ROR_SW_CLOSED   14  (I2)    amarelho    GPIO11  X X     GPIO08  verde       (I1)    15  ROR_MOUNT_PARKED

ROR_PARKED = 10
ROR_MOVE = 24
ROR_SW_CLOSED = 11
ROR_SW_OPEN = 25
ROR_MOUNT_PARKED = 8

ROR_AAGSAFE = 9

ROR_AAG_HOST = '192.168.0.205'
ROR_AAG_PORT = 80

PWR_RL1B = 18
PWR_RPI = 27
PWR_SCOPE = 22
PWR_MAIN = 23

PWR_RL1C = 17
PWR_RL2C = 04


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


class Pwr(object):

	log = logging.getLogger(__name__)
	log.setLevel(logging.DEBUG)
	handler = logging.handlers.SysLogHandler(address='/dev/log')
	formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
	handler.setFormatter(formatter)
	log.addHandler(handler)

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(PWR_RL1B, GPIO.OUT)
	GPIO.setup(PWR_RPI, GPIO.OUT)
	GPIO.setup(PWR_SCOPE, GPIO.OUT)
	GPIO.setup(PWR_MAIN, GPIO.OUT)

	GPIO.setup(PWR_RL1C, GPIO.OUT)
	GPIO.setup(PWR_RL2C, GPIO.OUT)

	def __init__(self):
		self._running = True

	def terminate(self):
		self._running = False

	@staticmethod
	def is_rl1b_closed():
		if GPIO.input(PWR_RL1B):
			return True
		return False

	@staticmethod
	def is_rl1b_open():
		if not GPIO.input(PWR_RL1B):
			return True
		return False

	def rl1b_close(self):
		self.log.debug('rl1b_close')
		if self.is_rl1b_open():
			GPIO.output(PWR_RL1B, GPIO.HIGH)
			return True
		return False

	def rl1b_open(self):
		self.log.debug('rl1b_open')
		if self.is_rl1b_closed():
			GPIO.output(PWR_RL1B, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def is_rpi_on():
		if GPIO.input(PWR_RPI):
			return True
		return False

	@staticmethod
	def is_rpi_off():
		if not GPIO.input(PWR_RPI):
			return True
		return False

	def rpi_on(self):
		self.log.debug('rpi_on')
		if self.is_rpi_off():
			GPIO.output(PWR_RPI, GPIO.HIGH)
			return True
		return False

	def rpi_off(self):
		self.log.debug('rpi_off')
		if self.is_rpi_on():
			GPIO.output(PWR_RPI, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def is_scope_on():
		if GPIO.input(PWR_SCOPE):
			return True
		return False

	@staticmethod
	def is_scope_off():
		if not GPIO.input(PWR_SCOPE):
			return True
		return False

	def scope_on(self):
		self.log.debug('scope_on')
		if self.is_scope_off():
			GPIO.output(PWR_SCOPE, GPIO.HIGH)
			return True
		return False

	def scope_off(self):
		self.log.debug('scope_off')
		if self.is_scope_on():
			GPIO.output(PWR_SCOPE, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def is_power_on():
		if GPIO.input(PWR_MAIN):
			return True
		return False

	@staticmethod
	def is_power_off():
		if not GPIO.input(PWR_MAIN):
			return True
		return False

	def power_on(self):
		self.log.debug('power_on')
		if self.is_power_off():
			GPIO.output(PWR_MAIN, GPIO.HIGH)
			return True
		return False

	def power_off(self):
		self.log.debug('power_off')
		if self.is_power_on():
			GPIO.output(PWR_MAIN, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def is_rl1c_closed():
		if GPIO.input(PWR_RL1C):
			return True
		return False

	@staticmethod
	def is_rl1c_open():
		if not GPIO.input(PWR_RL1C):
			return True
		return False

	def rl1c_close(self):
		self.log.debug('rl1c_close')
		if self.is_rl1c_open():
			GPIO.output(PWR_RL1C, GPIO.HIGH)
			return True
		return False

	def rl1c_open(self):
		self.log.debug('rl1c_open')
		if self.is_rl1c_closed():
			GPIO.output(PWR_RL1C, GPIO.LOW)
			return True
		return False

	# --------------------------

	@staticmethod
	def is_rl2c_closed():
		if GPIO.input(PWR_RL2C):
			return True
		return False

	@staticmethod
	def is_rl2c_open():
		if not GPIO.input(PWR_RL2C):
			return True
		return False

	def rl2c_close(self):
		self.log.debug('rl2c_close')
		if self.is_rl2c_open():
			GPIO.output(PWR_RL2C, GPIO.HIGH)
			return True
		return False

	def rl2c_open(self):
		self.log.debug('rl2c_open')
		if self.is_rl2c_closed():
			GPIO.output(PWR_RL2C, GPIO.LOW)
			return True
		return False


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
		return RoR._is_unparked() and RoR._is_not_open() and RoR._is_mount_parked() and RoR.is_safe() and RoR.is_aagsafe()

	@staticmethod
	def can_close():
		return RoR._is_unparked() and RoR.is_not_closed() and RoR._is_mount_parked()

	@staticmethod
	def can_park():
		# return RoR._is_unparked() and RoR._is_closed() and RoR._is_not_open()
		return RoR._is_closed() and RoR._is_not_open()

	@staticmethod
	def can_unpark():
		return RoR._is_parked() and RoR._is_mount_parked() and RoR.is_safe() and RoR.is_aagsafe()

	@staticmethod
	def _can_move():
		return RoR._is_unparked() and RoR._is_mount_parked()

	@staticmethod
	def _can_stop():
		return RoR.is_not_closed() and RoR._is_not_open()

	@staticmethod
	def is_aagsafe():
		if GPIO.input(ROR_AAGSAFE) == GPIO.HIGH:
			return True
		return False

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
		if self.can_unpark() and self.is_safe() and self.is_aagsafe():
			GPIO.output(ROR_PARKED, GPIO.HIGH)
			return True
		return False

	def open(self):
		self.log.debug('open')
		if self.can_open() and self.is_safe() and self.is_aagsafe():
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
		self.log.debug('parked:%s open:%s closed:%s mountParked:%s safe:%s aagsafe:%s / file: %s %s 0 ' % (
			self._is_parked(), self._is_open(), self._is_closed(), self._is_mount_parked(), self.is_safe(), self.is_aagsafe(), p, s))
		return '%s %s 0' % (p, s)


# --------------------------

# 200 OK
# 202 ACCEPTED
# 409 CONFLICT 

# --------------------------


@route('/', method='GET')
def index():
	response.content_type = 'text/html'
	response.status = 200
	return "REST Services - /ror = Roll-Off Roof Manager, /pwr = Power Manager"


@route('/ror/park', method='GET')
def ror_can_park():
	# response.status = 200 if RoR.is_not_closed() or RoR.can_park() else 409
	response.status = 200
	return


@route('/ror/park', method='PUT')
def ror_park():
	ror = RoR()
	p = multiprocessing.Process(target=ror.park)
	p.start()
	response.status = 202
	return


@route('/ror/unpark', method='GET')
def ror_can_unpark():
	response.status = 200 if RoR.can_unpark() else 409
	return


@route('/ror/unpark', method='PUT')
def ror_unpark():
	ror = RoR()
	p = multiprocessing.Process(target=ror.unpark)
	p.start()
	response.status = 202
	return


@route('/ror/open', method='GET')
def ror_can_open():
	response.status = 200 if RoR.can_open() else 409
	return


@route('/ror/open', method='PUT')
def ror_open():
	ror = RoR()
	p = multiprocessing.Process(target=ror.open)
	p.start()
	response.status = 202
	return


@route('/ror/close', method='GET')
def ror_can_close():
	response.status = 200 if RoR.can_close() else 409
	return


@route('/ror/close', method='PUT')
def ror_close():
	ror = RoR()
	p = multiprocessing.Process(target=ror.close)
	p.start()
	response.status = 202
	return


@route('/ror/abort', method='PUT')
def ror_abort():
	ror = RoR()
	p = multiprocessing.Process(target=ror.abort)
	response.status = 202
	p.start()
	return


@route('/ror/status', method='GET')
def ror_status():
	ror = RoR()
	response.content_type = 'text/html'
	response.status = 200
	return ror.status


@route('/ror/safe', method='GET')
def ror_is_safe():
	response.status = 200 if RoR.is_safe() else 409
	return


@route('/ror/aagsafe', method='GET')
def ror_is_aagsafe():
	response.status = 200 if RoR.is_aagsafe() else 409
	return

# --------------------------


@route('/rl1b/status', method='GET')
def rl1b_status():
	response.status = 200 if Pwr.is_rl1b_closed() else 409


@route('/rl1b/close', method='PUT')
def rl1b_close():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.rl1b_close)
	p.start()
	response.status = 202
	return


@route('/rl1b/open', method='PUT')
def rl1b_open():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.rl1b_open)
	p.start()
	response.status = 202
	return


@route('/rl1c/status', method='GET')
def rl1c_status():
	response.status = 200 if Pwr.is_rl1c_closed() else 409


@route('/rl1c/close', method='PUT')
def rl1c_close():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.rl1c_close)
	p.start()
	response.status = 202
	return


@route('/rl1c/open', method='PUT')
def rl1c_open():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.rl1c_open)
	p.start()
	response.status = 202
	return


@route('/rl2c/status', method='GET')
def rl2c_status():
	response.status = 200 if Pwr.is_rl2c_closed() else 409


@route('/rl2c/close', method='PUT')
def rl2c_close():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.rl2c_close)
	p.start()
	response.status = 202
	return


@route('/rl2c/open', method='PUT')
def rl2c_open():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.rl2c_open)
	p.start()
	response.status = 202
	return


# --------------------------

@route('/rpi/status', method='GET')
def pwr_rpi_status():
	response.status = 200 if Pwr.is_rpi_on() else 409


@route('/rpi/on', method='PUT')
def pwr_rpi_on():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.rpi_on)
	p.start()
	response.status = 202
	return


@route('/rpi/off', method='PUT')
def pwr_rpi_off():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.rpi_off)
	p.start()
	response.status = 202
	return


# --------------------------

@route('/scope/status', method='GET')
def pwr_scope_status():
	response.status = 200 if Pwr.is_scope_on() else 409


@route('/scope/on', method='PUT')
def pwr_scope_on():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.scope_on)
	p.start()
	response.status = 202
	return


@route('/scope/off', method='PUT')
def pwr_scope_off():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.scope_off)
	p.start()
	response.status = 202
	return


# --------------------------

@route('/power/status', method='GET')
def pwr_power_status():
	response.status = 200 if Pwr.is_power_on() else 409


@route('/power/on', method='PUT')
def pwr_power_on():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.power_on)
	p.start()
	response.status = 202
	return


@route('/power/off', method='PUT')
def pwr_power_off():
	pwr = Pwr()
	p = multiprocessing.Process(target=pwr.power_off)
	p.start()
	response.status = 202
	return

# --------------------------


if __name__ == "__main__":
	# t = Timer(10, rotina para fazer pooling do aagcw)
	# t.run()
	run(host='0.0.0.0', port=80, server='gevent')
