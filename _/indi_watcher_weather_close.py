#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import time
import logging
import PyIndi

class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('IndiClient')
    def newDevice(self, d):
        pass
    def newProperty(self, p):
        pass
    def removeProperty(self, p):
        pass
    def newBLOB(self, bp):
        pass
    def newSwitch(self, svp):
        pass
    def newNumber(self, nvp):
        pass
    def newText(self, tvp):
        pass
    def newLight(self, lvp):
        pass
    def newMessage(self, d, m):
        pass
    def serverConnected(self):
        self.logger.info("indiserver Connected")
    def serverDisconnected(self, code):
        self.logger.info("indiserver Disconnected, exiting.")
        sys.exit(1)
    def log(self, message):
        self.logger.info(message)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

indiclient=IndiClient()
indiclient.setServer("localhost",7624)
 
if (not(indiclient.connectServer())):
     indiclient.log("No indiserver running, exiting.")
     sys.exit(1)

device_name="AAG Solo Weather"
device=None
connection_name="CONNECTION"
connection=None

while not(device):
    device=indiclient.getDevice(device_name)
    time.sleep(0.2)
    if (device):
        indiclient.log("DEVICE READY - device")
        connection=None
     
while device and \
      not(connection):
    connection=device.getSwitch(connection_name)
    time.sleep(0.2)
    if (connection):
        indiclient.log("SWITCH READY - connection")

if device and \
   connection and \
   device.isConnected():
    connection[0].s=PyIndi.ISS_OFF
    connection[1].s=PyIndi.ISS_ON
    indiclient.sendNewSwitch(connection)
    indiclient.log("DEVICE DICONNECTED")

