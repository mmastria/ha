#!/usr/bin/python
# -*- coding: UTF-8 -*-

import multiprocessing 
import RPi.GPIO as GPIO
from time import sleep
from gevent import monkey
from bottle import route, response, run
import logging.handlers

monkey.patch_all()


# PWR_EAST = 17
# PWR_WEST = 27

ROR_PARKED = 22
ROR_MOVE = 23
ROR_SW_CLOSED = 24
ROR_SW_OPEN = 25
ROR_MOUNT_PARKED = 26


# ROR_AAGCW = ??
# ROR_PWR_SOURCE = ??


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
        return RoR._is_unparked() and RoR._is_not_open() and RoR._is_mount_parked()

    @staticmethod
    def can_close():
        return RoR._is_unparked() and RoR.is_not_closed() and RoR._is_mount_parked()

    @staticmethod
    def can_park():
        return RoR._is_unparked() and RoR._is_closed() and RoR._is_not_open()

    @staticmethod
    def _can_unpark():
        return RoR._is_parked() and RoR._is_mount_parked()

    @staticmethod
    def _can_move():
        return RoR._is_unparked() and RoR._is_mount_parked()

    @staticmethod
    def _can_stop():
        return RoR.is_not_closed() and RoR._is_not_open()

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
        if self._can_unpark():
            GPIO.output(ROR_PARKED, GPIO.HIGH)
            return True
        return False

    def open(self):
        self.log.debug('open')
        if self.can_open():
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
        m = '1' if self._is_mount_parked() else '0'
        self.log.debug('-- parked: %s (p:%s) - open: %s - closed: %s (s:%s) - mount_parked: %s (m:%s)' % (
            self._is_parked(), p, self._is_open(), self._is_closed(), s, self._is_mount_parked(), m))
        return '%s %s 0' % (p, s)

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
    response.status = 200 if RoR.is_not_closed() or RoR.can_park() else 409
    return


@route('/park', method='PUT')
def park():
    ror = RoR()
    p = multiprocessing.Process(target=ror.park)
    p.start()
    response.status = 202
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


# --------------------------


if __name__ == "__main__":

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    log.debug("starting roll-off roof controller")
    run(host='0.0.0.0', port=80, server='gevent')
