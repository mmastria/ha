#!/usr/bin/python
import serial
import sys
import time
import os
import subprocess

timeout = 100
handshaking = '\x21\x11\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x30'
hschar = '\x11'
RESP_V = '!w          000'

def talk(src, sname, dest, dname):
    inByte = ''
    src_req = '' 
    while src.inWaiting() > 0:
        inByte = src.read(1)
        if inByte == '':
            break;
        src_req += inByte
        if inByte == '!':
            break;
    if inByte == '!':
        print '\n' + sname + ' >> [' + src_req + ']'
        print ' '*len(sname)+'    [' + ':'.join(x.encode('hex') for x in src_req) + ']'
        if src_req == 'V!':
            dest_resp = RESP_V + handshaking 
        else:
            dest.write(src_req)
            time.sleep(0.1)
            dest_resp = ''
            timeout = 100
            if src_req == 'E!' or src_req == 'h!' or src_req == 't!':
                time.sleep(0.2)
                timeout *= 3
            while dest.inWaiting() == 0 and timeout > 0:
                time.sleep(0.001)
                timeout -= 1
            while dest.inWaiting() > 0:
                inByte = dest.read(1)
                if not (dest_resp == '' and inByte != '!'):
                    dest_resp += inByte
                else:
                    print ' '*len(sname) + ' ## [' + inByte + '] discarding - hex [' + inByte.encode('hex') + ']'
        if len(dest_resp) >= 15 and len(dest_resp) % 15 == 13 and dest_resp[-13:]+' 0'==handshaking:
            dest_resp += ' 0'
        if len(dest_resp) >= 15 and len(dest_resp) % 15 == 14 and dest_resp[-14:]+'0'==handshaking:
            dest_resp += '0'
        if len(dest_resp) >= 15 and len(dest_resp) % 15 == 0 and dest_resp[-15:]==handshaking:
            print sname + ' << [' + dest_resp.replace(hschar,'_') + ']'
            print ' '*len(sname)+'    [' + ':'.join(x.encode('hex') for x in dest_resp) + ']'
            src.write(dest_resp)
        else:
            print sname + ' <# [' + dest_resp.replace(hschar,'_').replace(' ','.') + ']'
            print ' '*len(sname)+'    [' + ':'.join(x.encode('hex') for x in dest_resp) + ']'
            print sname + ' <= [' + handshaking.replace(hschar,'_') + ']'
            print ' '*len(sname)+'    [' + ':'.join(x.encode('hex') for x in handshaking) + ']'
            src.write(handshaking)
        time.sleep(0.1)

def connect(fport, name):
    dev = serial.Serial(
        port = fport,
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
    if not dev.isOpen():
        print '... can\'t connect to ' + name + ' at ' + fport + ', exiting.'
        sys.exit()
    print '... connected to ' + name + ' - ' + fport
    dev.flushInput()
    dev.flushOutput()
    return dev

def createVPort(fPortServer, fPortClient):
    cmd=['/usr/bin/socat','-d','-d','PTY,link='+fPortServer+',b9600,rawer','PTY,link='+fPortClient+',b9600,rawer']
    fproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    return fproc

def destroyVPort(fproc):
    vproc.kill()

def main():

    print '\nInitializing Serial Multiplex'

    proc = createVPort('/dev/ttyUSB1', '/dev/ttyUSB2')

    watcher = connect( '/dev/ttyUSB0', 'AAG Cloud Watcher' ) 
    solo = connect( '/dev/ttyAMA0', 'AAG Solo')
    indi = connect( '/dev/ttyUSB1', 'Indi' )


    print 'Serial Multiplex running...'
    while True:

        # AAG Solo <--> AAG Clowd Watcher
        talk( solo, 'solo', watcher, 'watcher')

        # Indi Driver <--> AAG Clowd Watcher
        talk( indi, 'indi', watcher, 'watcher')

if __name__ == '__main__':
    main()
    destroyVPort(proc)
