#!/usr/bin/python
import serial
import sys
import time
from SerialEmulator import SerialEmulator

def main():

    #print "\nInitializing serial relay connection"

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

    indi = SerialEmulator('./ttydevice','/dev/ttyUSB9') 

    if not watcher.isOpen():
        sys.exit()

    if not solo.isOpen():
        sys.exit()

    watcher.flushInput()
    watcher.flushOutput()

    solo.flushInput()
    solo.flushOutput()

    while True:

        solo_req = ''
        inByte = ''
        while solo.inWaiting() > 0:
            inByte = solo.read(1)
            solo_req += inByte
            if inByte == '!':
                break;
        if inByte == '!':
            #print "solo >> " + solo_req
            watcher.write(solo_req)
            time.sleep(0.1)
            watcher_resp = ''
            while watcher.inWaiting() == 0:
                pass
            while watcher.inWaiting() > 0:
                watcher_resp += watcher.read(1)
            if watcher_resp != '':
                #print "wtch << " + watcher_resp
                solo.write(watcher_resp)
                time.sleep(0.1)

        #indi_req = ''
        #inByte = indi.read()
        while False and inByte:
            indi_req += inByte
            if inByte == '!':
                break;
            inByte = indi.read()
        if False and inByte == '!':
            print "indi >> " + indi_req
            watcher.write(indi_req)
            time.sleep(0.1)
            watcher_resp = ''
            while watcher.inWaiting() == 0:
                pass
            while watcher.inWaiting() > 0:
                watcher_resp += watcher.read(1)
            if watcher_resp != '':
                print "wtch << " + watcher_resp
                indi.write(watcher_resp)
                time.sleep(0.1)


if __name__ == "__main__":
    main()

