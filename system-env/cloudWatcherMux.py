#!/usr/bin/python
# -*- coding: UTF-8 -*-

import serial
import sys
import time
import os
import subprocess

timeout     = 100
handshaking = '\x21\x11\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x30'
kresponse   = '\x21\x4b\x21\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
mresponse   = '\x21\x4d\x21\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
hschar      = '\x11'
RESP_V      = '!w          000'
RESP_K      = '!K1198\x20\x20\x20\x20\x20\x20\x20\x20\x20'
RESP_M      = '!M\x01\x22\x07\xD0\x02\x30\x0D\x7A\x00\x0A\x00\x0A\x00'

# RESP_K
# Internal Serial No         = 1198

# RESP_M
# Zener voltage              =  2.9 * 10 =  290 = x01 x22
# LDR Max Resistance (K)     = 2000 *  1 = 2000 = x07 xD0
# LDR PullUp Resistance (K)  =   56 * 10 =  560 = x02 x30
# Rain Beta Factor           = 3450 *  1 = 3450 = x0D x7A
# Rain Resistance at 25 (K)  =    1 * 10 =   10 = x00 x0A 
# Rain PullUp Resistance (K) =    1 * 10 =   10 = x00 x0A

# Firmware ver. 5.70

def talk(src, sname, dest, dname):
    inByte = ''
    src_req = '' 
    while src.inWaiting() > 0:
        inByte = src.read(1)
        if len(inByte) == 0:
            break;
        src_req += inByte
        if inByte == '!':
            break;
    if inByte == '!':
        #print '\n' + sname + ' >> [' + src_req + ']'
        #print ' '*len(sname)+'    [' + ':'.join(x.encode('hex') for x in src_req) + ']'
        if src_req == 'V!':
            dest_resp = RESP_V + handshaking
        else:
            dest.write(src_req)
            time.sleep(0.1)
            dest_resp = ''
            timeout = 100
            if src_req == 'E!' or src_req == 'h!' or src_req == 't!' or src_req == 'M!' or src_req == 'K!':
                time.sleep(0.1)
                timeout *= 3
            while dest.inWaiting() == 0 and timeout > 0:
                time.sleep(0.001)
                timeout -= 1
            while dest.inWaiting() > 0:
                inByte = dest.read(1)
                time.sleep(0.01)
                if not (dest_resp == '' and inByte != '!'):
                    dest_resp += inByte
                #else:
                    #print ' '*len(sname) + ' ## [' + inByte + '] discarding - hex [' + inByte.encode('hex') + ']'
        if len(dest_resp) >= 15 and len(dest_resp) % 15 == 13 and dest_resp[-13:]+' 0' == handshaking:
            dest_resp += ' 0'
        if len(dest_resp) >= 15 and len(dest_resp) % 15 == 14 and dest_resp[-14:]+'0' == handshaking:
            dest_resp += '0'
        if len(dest_resp) >= 15 and len(dest_resp) % 15 == 0 and dest_resp[-15:] == handshaking:
            if src_req == 'K!' and dest_resp == kresponse + handshaking:
                #print sname + ' <# [' + dest_resp.replace(hschar,'_').replace(' ','.') + ']'
                dest_resp = RESP_K + handshaking 
            if src_req == 'M!' and dest_resp == mresponse + handshaking:
                #print sname + ' <# [' + dest_resp.replace(hschar,'_').replace(' ','.') + ']'
                dest_resp = RESP_M + handshaking 
            #print sname + ' << [' + dest_resp.replace(hschar,'_') + ']'
            #print ' '*len(sname)+'    [' + ':'.join(x.encode('hex') for x in dest_resp) + ']'
            src.write(dest_resp)
        else:
            #print sname + ' <# [' + dest_resp.replace(hschar,'_').replace(' ','.') + ']'
            #print ' '*len(sname)+'    [' + ':'.join(x.encode('hex') for x in dest_resp) + ']'
            #print sname + ' <= [' + handshaking.replace(hschar,'_') + ']'
            #print ' '*len(sname)+'    [' + ':'.join(x.encode('hex') for x in handshaking) + ']'
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
    time.sleep(0.5)
    cmd=['/bin/stty','-F', fPortServer, '9600']
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.5)
    cmd=['/bin/stty','-F', fPortClient, '9600']
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.5)
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
    try:
        main()
    except:
        pass
    try:
        destroyVPort(proc)
    except:
        pass
    print '\nSerial Multiplex ended!\n'

