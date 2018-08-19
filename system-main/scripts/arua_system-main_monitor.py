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
indiclient.setServer("localhost",7624)
 
if (not(indiclient.connectServer())):
     indiclient.log("No indiserver running, exiting.")
     sys.exit(1)
 
astrometry="Astrometry"
astrometry_connection="CONNECTION"
solver="ASTROMETRY_SOLVER"
device_astrometry=None
astrometry_switch_connection=None
switch_solver=None

while True:

    nsleep=0

    # ----------------------------------

    while not(device_astrometry):
        device_astrometry=indiclient.getDevice(astrometry)
        astrometry_switch_connection=None
        time.sleep(0.2)
     
    while device_astrometry and \
          not(astrometry_switch_connection):
        astrometry_switch_connection=device_astrometry.getSwitch(astrometry_connection)
        time.sleep(0.2)

    if device_astrometry and \
       astrometry_switch_connection and \
       not(device_astrometry.isConnected()):
        astrometry_switch_connection[0].s=PyIndi.ISS_ON
        astrometry_switch_connection[1].s=PyIndi.ISS_OFF
        indiclient.sendNewSwitch(astrometry_switch_connection)
        switch_solver=None
        time.sleep(0.2)

    while device_astrometry and \
          astrometry_switch_connection and \
          device_astrometry.isConnected() and \
          not(switch_solver):
        switch_solver=device_astrometry.getSwitch(solver)
        time.sleep(0.2)

    # ----------------------------------
    time.sleep(0.9-min(nsleep*0.2, 0.8))
    # ----------------------------------

    if device_astrometry and \
       astrometry_switch_connection and \
       device_astrometry.isConnected() and \
       switch_solver and \
       len(switch_solver) > 0 and \
       switch_solver[0] is not None \
       and switch_solver[0].s == PyIndi.ISS_OFF:
        switch_solver[0].s=PyIndi.ISS_ON
        switch_solver[1].s=PyIndi.ISS_OFF
        indiclient.sendNewSwitch(switch_solver)

    # ----------------------------------

