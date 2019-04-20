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

class EnvSafe(object):

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



# curl -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiYzk4ZWJlZjdkM2Q0ZjE4ODY1ODllYWFiNjg3OGNhNCIsImlhdCI6MTU1NTYyNzIzNiwiZXhwIjoxODcwOTg3MjM2fQ.jbOcr4Pmh9F2c0YD7Qzb87MHxsorUKmgipuVdJpwwxI" -H "Content-Type: application/json" http://hassio.arua:8123/api/states/binary_sensor.obs_alert|jq

# r = requests.get('<MY_URI>', headers={'Authorization': 'TOK:<MY_TOKEN>'})


	@staticmethod
	def is_safe():
		values = {}
		try:
			url = "http://{}:{}/".format(ROR_AAG_HOST, ROR_AAG_PORT)
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
	def status(self):
            status = {}
            status['safe'] = self.is_safe()
            return status

@route('/', method='GET')
def index():
	response.content_type = 'text/html'
	response.status = 200
	return "REST Services - /status - Environment Status"

@route('/status', method='GET')
def ror_reststatus():
	ror = RoR()
        response.content_type = 'application/json'
	response.status = 200
	return json.dumps(ror.reststatus)

# --------------------------

if __name__ == "__main__":
	run(host='0.0.0.0', port=80, server='gevent')
