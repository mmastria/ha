#!/usr/bin/python
# -*- coding: UTF-8 -*-

import multiprocessing
from time import sleep
from gevent import monkey
from bottle import route, response, run
import requests
import json
import logging.handlers

monkey.patch_all()

class RoR(object):

	log = logging.getLogger(__name__)
	log.setLevel(logging.DEBUG)
	handler = logging.handlers.SysLogHandler(address='/dev/log')
	formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
	handler.setFormatter(formatter)
	log.addHandler(handler)

	def __init__(self):
		self._running = True

	def terminate(self):
		self._running = False

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

	@property
	def reststatus(self):
            status = {}
            status['parked'] = self._is_parked()
            status['open'] = self._is_open()
            status['closed'] = self._is_closed()
            status['mount_parked'] = self._is_mount_parked()
            status['safe'] = self.is_safe()
            status['aagsafe'] = self.is_aagsafe()
            return status

@route('/', method='GET')
def index():
	response.content_type = 'text/html'
	response.status = 200
	return "REST Services - /ror = Roll-Off Roof Manager, /status = Rest Status"


@route('/ror/close', method='GET')
def ror_can_close():
	response.status = 200 if RoR.can_close() else 409
	return

@route('/ror/status', method='GET')
def ror_status():
	ror = RoR()
	response.content_type = 'text/html'
	response.status = 200
	return ror.status

@route('/status', method='GET')
def ror_reststatus():
	ror = RoR()
        response.content_type = 'application/json'
	response.status = 200
	return json.dumps(ror.reststatus)

# --------------------------

if __name__ == "__main__":
	# t = Timer(10, rotina para fazer pooling do aagcw)
	# t.run()
	run(host='0.0.0.0', port=80, server='gevent')
