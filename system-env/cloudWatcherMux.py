#!/usr/bin/python
import serial
import sys
import time
import os
import subprocess

def main():

    print "\nInitializing serial relay connection"

    watcher = serial.Serial(
        port = '/dev/ttyUSB0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        xonxoff = False,
        rtscts = False,
        dsrdtr = False,
        writeTimeout = 2,
        timeout = 2 
    )

    solo = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        xonxoff = False,
        rtscts = False,
        dsrdtr = False,
        writeTimeout = 2,
        timeout = 2 
    )

    if not watcher.isOpen():
        sys.exit()

    if not solo.isOpen():
        sys.exit()

    cmd=['/usr/bin/socat','-d','-d','PTY,link=/dev/ttyUSB1,raw,echo=0','PTY,link=/dev/ttyUSB2,raw,echo=0']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)

    indi = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        xonxoff = False,
        rtscts = False,
        dsrdtr = False,
        writeTimeout = 2,
        timeout = 2 
    )

    if not indi.isOpen():
        sys.exit()

    watcher.flushInput()
    watcher.flushOutput()

    solo.flushInput()
    solo.flushOutput()

    indi.flushInput()
    indi.flushOutput()

    solo_req = "" 
    indi_req = ""

    while True:

        inByte = ''
        while solo.inWaiting() > 0:
            inByte = solo.read(1)
            solo_req += inByte
            if inByte == '!':
                break;
        if inByte == '!':
            print "solo >> " + solo_req
            watcher.write(solo_req)
            solo_req = "" 
            time.sleep(0.1)
            watcher_resp = ""
            while watcher.inWaiting() == 0:
                pass
            while watcher.inWaiting() > 0:
                watcher_resp += watcher.read(1)
            if watcher_resp != '':
                print "solo << " + watcher_resp
                solo.write(watcher_resp)
                time.sleep(0.1)

        inByte = '' 
        while indi.inWaiting() > 0:
            inByte = indi.read(1)
            indi_req += inByte
            if inByte == '!':
                break;
        if inByte == '!':
            print "indi >> " + indi_req
            watcher.write(indi_req)
            indi_req = ""
            time.sleep(0.1)
            watcher_resp = ""
            while watcher.inWaiting() == 0:
                pass
            while watcher.inWaiting() > 0:
                watcher_resp += watcher.read(1)
            if watcher_resp != '':
                print "indi << " + watcher_resp
                indi.write(watcher_resp)
                time.sleep(0.1)

if __name__ == "__main__":
    main()
    proc.kill() 
