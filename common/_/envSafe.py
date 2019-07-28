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

HASSIO_HOST = 'hassio.arua'
HASSIO_PORT = 8123
HASSIO_AUTH = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiYzk4ZWJlZjdkM2Q0ZjE4ODY1ODllYWFiNjg3OGNhNCIsImlhdCI6MTU1NTYyNzIzNiwiZXhwIjoxODcwOTg3MjM2fQ.jbOcr4Pmh9F2c0YD7Qzb87MHxsorUKmgipuVdJpwwxI'

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

	@staticmethod
	def is_safe():
            try:
	        url = "http://{}:{}/api/states/binary_sensor.obs_alert".format(HASSIO_HOST, HASSIO_PORT)
                resp = requests.get(url, headers={'Authorization': 'Bearer {}'.format(HASSIO_AUTH), 'Content-Type': 'application/json'}, timeout=5)
                rjson = resp.json()
                state = rjson['state']
		if state == u'on':
		    return False
		else:
		    return True
	    except:
                #self.log.debug('Erro de conexao')
		return False

	@property
	def status(self):
            status = {}
            status['roof_status'] = {}
            status['roof_status']['open_ok'] = 1 if self.is_safe() else 0
            status['roof_status']['reasons'] = '- se indicar unsafe encerre as atividades -'
            return status

@route('/', method='GET')
def index():
	response.content_type = 'text/html'
	response.status = 200
	return "REST Services - /status - Environment Status"

@route('/status', method='GET')
def status():
	envsafe = EnvSafe()
        response.content_type = 'application/json'
	response.status = 200
	return json.dumps(envsafe.status)

# --------------------------

if __name__ == "__main__":
	run(host='0.0.0.0', port=81, server='gevent')
