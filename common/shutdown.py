#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import time
import logging
import PyIndi

def strISState(s):
    if (s == PyIndi.ISS_OFF):
        return "Off"
    else:
        return "On"
def strIPState(s):
    if (s == PyIndi.IPS_IDLE):
        return "Idle"
    elif (s == PyIndi.IPS_OK):
        return "Ok"
    elif (s == PyIndi.IPS_BUSY):
        return "Busy"
    elif (s == PyIndi.IPS_ALERT):
        return "Alert"

class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('IndiClient')
#        self.logger.info('creating an instance of IndiClient')
    def newDevice(self, d):
        pass
#        self.logger.info("new device " + d.getDeviceName())
    def newProperty(self, p):
        pass
#        self.logger.info("new property "+ p.getName() + " for device "+ p.getDeviceName())
    def removeProperty(self, p):
        pass
#        self.logger.info("remove property "+ p.getName() + " for device "+ p.getDeviceName())
    def newBLOB(self, bp):
        pass
#        self.logger.info("new BLOB "+ bp.name.decode())
    def newSwitch(self, svp):
        pass
#        self.logger.info ("new Switch "+ svp.name.decode() + " for device "+ svp.device.decode())
    def newNumber(self, nvp):
        pass
#        self.logger.info("new Number "+ nvp.name.decode() + " for device "+ nvp.device.decode())
    def newText(self, tvp):
        pass
#        self.logger.info("new Text "+ tvp.name.decode() + " for device "+ tvp.device.decode())
    def newLight(self, lvp):
        pass
#        self.logger.info("new Light "+ lvp.name.decode() + " for device "+ lvp.device.decode())
    def newMessage(self, d, m):
        pass
#        try:
#                self.logger.info("new Message "+ d.messageQueue(m).decode())
#        except:
#                self.logger.info("new Message d.messageQueue(m).decode() error")
    def serverConnected(self):
        pass
#        self.logger.info("Server connected ("+self.getHost()+":"+str(self.getPort())+")")
    def serverDisconnected(self, code):
        pass
#        self.logger.info("Server disconnected (exit code = "+str(code)+","+str(self.getHost())+":"+str(self.getPort())+")")


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

#obs=IndiClient()
east=IndiClient()
west=IndiClient()

#obs.setServer("localhost",7624)
east.setServer("system-east.arua",7624)
west.setServer("system-west.arua",7624)

print("-----------------")
print("-- connecting")
print("-----------------")
#if (not(obs.connectServer())):
#     print("No indiserver running on "+obs.getHost()+":"+str(obs.getPort())+" - Exiting")
#     sys.exit(1)
#else:
#     print("- "+obs.getHost()+":"+str(obs.getPort())+" - ok")

if (not(east.connectServer())):
     print("No indiserver running on "+east.getHost()+":"+str(east.getPort())+" - Exiting")
     sys.exit(1)
else:
     print("- "+east.getHost()+":"+str(east.getPort())+" - ok")

if (not(west.connectServer())):
     print("No indiserver running on "+west.getHost()+":"+str(west.getPort())+" - Exiting")
     sys.exit(1)
else:
     print("- "+west.getHost()+":"+str(west.getPort())+" - ok")

print("-----------------")
print("-- delay")
print("-----------------")
time.sleep(5)

#print("-----------------")
#dl=obs.getDevices()
#for dev in dl:
#    print(dev.getDeviceName())

print("-----------------")
dl=east.getDevices()
for dev in dl:
    print(dev.getDeviceName())

print("-----------------")
dl=west.getDevices()
for dev in dl:
    print(dev.getDeviceName())

print("-----------------")
