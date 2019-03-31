#!/usr/bin/python
import serial
import sys
import time
import os
import subprocess

def main():

    print '\nInitializing serial relay connection'

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
    print '... connected to AAG Cloud Watcher - /dev/ttyUSB0'

    if not solo.isOpen():
        sys.exit()
    print '... connected to AAG Solo - /dev/ttyAMA0' 


    cmd=['/usr/bin/socat','-d','-d','PTY,link=/dev/ttyUSB1,b9600,rawer','PTY,link=/dev/ttyUSB2,b9600,rawer']
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
    print '... connected to Indi - /dev/ttyUSB1 loop /dev/ttyUSB2'

    watcher.flushInput()
    watcher.flushOutput()

    solo.flushInput()
    solo.flushOutput()

    indi.flushInput()
    indi.flushOutput()

    solo_req = '' 
    indi_req = ''

    print '... cleared buffers'

    timeout = 100
    handshaking = '\x21\x11\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x30'
   
    RESP_V = '!w          000'

    while True:

        # AAG Solo <--> AAG Clowd Watcher

        inByte = ''
        while solo.inWaiting() > 0:
            inByte = solo.read(1)
            if inByte == '':
                break;
            solo_req += inByte
            if inByte == '!':
                break;
        if inByte == '!':
            #print '\nsolo >> ' + solo_req
            watcher.write(solo_req)
            time.sleep(0.1)
            watcher_resp = ''
            timeout = 100
            if solo_req == 'E!':
                time.sleep(0.2)
                timeout *= 3
            solo_req = '' 
            while watcher.inWaiting() == 0 and timeout > 0:
                time.sleep(0.001)
                timeout -= 1
            while watcher.inWaiting() > 0:
                inByte = watcher.read(1)
                if not (watcher_resp == '' and inByte != '!'):
                    watcher_resp += inByte
            if len(watcher_resp) >= 15 and len(watcher_resp) % 15 == 13 and watcher_resp[-13:]+' 0'==handshaking:
                watcher_resp += ' 0'
            if len(watcher_resp) >= 15 and len(watcher_resp) % 15 == 14 and watcher_resp[-14:]+'0'==handshaking:
                watcher_resp += '0'
            if len(watcher_resp) >= 15 and len(watcher_resp) % 15 == 0 and watcher_resp[-15:]==handshaking:
                print 'solo << ' + watcher_resp
                solo.write(watcher_resp)
            else:
                #print 'solo <# ' + watcher_resp.replace(' ','.')
                #print 'solo <= ' + handshaking
                solo.write(handshaking)
            time.sleep(0.1)

        # Indi Driver <--> AAG Clowd Watcher

        inByte = '' 
        while indi.inWaiting() > 0:
            inByte = indi.read(1)
            if inByte == '':
                break;
            indi_req += inByte
            if inByte == '!':
                break;
        if inByte == '!':
            print '\nindi >> ' + indi_req
            if indi_req == 'V!':
                watcher_resp = RESP_V + handshaking 
            else:
                watcher.write(indi_req)
                time.sleep(0.1)
                watcher_resp = ''
                timeout = 100
                if indi_req == 'E!':
                    time.sleep(0.2)
                    timeout *= 3
                while watcher.inWaiting() == 0 and timeout > 0:
                    time.sleep(0.001)
                    timeout -= 1
                while watcher.inWaiting() > 0:
                    inByte = watcher.read(1)
                    if not (watcher_resp == '' and inByte != '!'):
                        watcher_resp += inByte
                if len(watcher_resp) >= 15 and len(watcher_resp) % 15 == 13 and watcher_resp[-13:]+' 0'==handshaking:
                    watcher_resp += ' 0'
                if len(watcher_resp) >= 15 and len(watcher_resp) % 15 == 14 and watcher_resp[-14:]+'0'==handshaking:
                    watcher_resp += '0'
            indi_req = ''
            if len(watcher_resp) >= 15 and len(watcher_resp) % 15 == 0 and watcher_resp[-15:]==handshaking: 
                print 'indi << ' + watcher_resp
                indi.write(watcher_resp)
            else:
                print 'indi <# ' + watcher_resp.replace(' ','.')
                print 'indi <= ' + handshaking
                indi.write(handshaking)
            time.sleep(0.1)

if __name__ == '__main__':
    main()
    proc.kill() 
