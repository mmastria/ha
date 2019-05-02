#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import multiprocessing
#import RPi.GPIO as GPIO
#from time import sleep
from gevent import monkey
from bottle import route, response, run
import requests
import json
import logging.handlers

monkey.patch_all()

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


class Indi(object):

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

	def getprop(self):
            data = {}
            try:
                s = subprocess.Popen('indi_getprop -h system-obs',shell=True, stdin=None, stdout=subprocess.PIPE, close_fds=True)
                t = s.stdout.read()
                s.wait()
                for device, value in [(pair.split("=")) for pair in t.replace('==','=').splitlines()]:
                    key = data 
                    prop = device.split('.')[-1]
                    for k in device.split('.'):
                        if not k in key:
                            if not k == prop:
                                key[k] = {}
                                key = key[k]
                            else:
                                key[k] = value
                        else:
                            key = key[k]
            except:
                pass
            return data 

@route('/', method='GET')
def index():
	response.content_type = 'text/html'
	response.status = 200
	return "Indi REST Services - /getprop = Get Devices Properties"


@route('/getprop', method='GET')
def indi_getprop():
	indi = Indi()
        r = json.dumps(indi.getprop())
        response.content_type = 'application/json'
	response.status = 200
        response['Content-Length'] = len(r)
	return r

# --------------------------

if __name__ == "__main__":
	# t = Timer(10, rotina para fazer pooling)
	# t.run()
	run(host='0.0.0.0', port=8080, server='gevent')
