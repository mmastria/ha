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
        #self.logger.info("newDevice")
        pass
    def newProperty(self, p):
        #self.logger.info("newProperty")
        pass
    def removeProperty(self, p):
        #self.logger.info("removeProperty")
        pass
    def newBLOB(self, bp):
        #self.logger.info("newBLOB")
        pass
    def newSwitch(self, svp):
        #self.logger.info("newSwitch")
        pass
    def newNumber(self, nvp):
        #self.logger.info("newNumber")
        pass
    def newText(self, tvp):
        #self.logger.info("newText "+tvp.name+" - device:"+tvp.device)
        pass
    def newLight(self, lvp):
        #self.logger.info("newLight")
        pass
    def newMessage(self, d, m):
        #self.logger.info("newMessage")
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
indiclient.setServer("localhost",7625)
 
if (not(indiclient.connectServer())):
     indiclient.log("No indiserver running, exiting.")
     sys.exit(1)
 
rolloffroof="RollOff Roof"
rolloffroof_connection="CONNECTION"

roof="ROOF"

device_rolloffroof=None

rolloffroof_switch_connection=None

switch_roof=None

while True:

    nsleep=0

    # ----------------------------------

    while not(device_rolloffroof):
        device_rolloffroof=indiclient.getDevice(rolloffroof)
        nsleep+=1
        time.sleep(0.2)
        if (device_rolloffroof):
            indiclient.log("DEVICE READY - device_rolloffroof ")
            rolloffroof_switch_connection=None
     
    while device_rolloffroof and \
          not(rolloffroof_switch_connection):
        rolloffroof_switch_connection=device_rolloffroof.getSwitch(rolloffroof_connection)
        nsleep+=1
        time.sleep(0.2)
        if (rolloffroof_switch_connection):
            indiclient.log("SWITCH READY - rolloffroof_switch_connection ")

    while device_rolloffroof and \
          rolloffroof_switch_connection and \
          not(device_rolloffroof.isConnected()):
        rolloffroof_switch_connection[0].s=PyIndi.ISS_ON
        rolloffroof_switch_connection[1].s=PyIndi.ISS_OFF
        indiclient.sendNewSwitch(rolloffroof_switch_connection)
        time.sleep(0.2)
        if (device_rolloffroof.isConnected()):
            indiclient.log("DEVICE CONNECTED / SWITCH ON - device_rolloffroof / rolloffroof_switch_connection ")
            switch_roof=None
        nsleep+=1

    while device_rolloffroof and \
          rolloffroof_switch_connection and \
          device_rolloffroof.isConnected() and \
          not(switch_roof):
        switch_roof=device_rolloffroof.getSwitch(roof)
        nsleep+=1
        time.sleep(0.2)
        if (switch_roof):
            indiclient.log("SWITCH READY - switch_roof ")

    # ----------------------------------
    time.sleep(1-min(nsleep*0.2, 0.8))
    # ----------------------------------

    if device_rolloffroof and \
       rolloffroof_switch_connection and \
       device_rolloffroof.isConnected() and \
       switch_roof and \
       len(switch_roof) > 0 and \
       switch_roof[0] is not None \
       and switch_roof[0].s == PyIndi.ISS_ON:
        indiclient.log("Roof Swith pressed, waiting 1/2 second") 
        time.sleep(0.5)
        indiclient.log("Turning off Roof Swith") 
        switch_roof[0].s=PyIndi.ISS_OFF
        switch_roof[1].s=PyIndi.ISS_ON
        indiclient.sendNewSwitch(switch_roof)

    # ----------------------------------


