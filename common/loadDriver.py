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

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    indiclient=IndiClient()
    indiclient.setServer("localhost",7624)
 
    if (not(indiclient.connectServer())):
        indiclient.log("No indiserver running, exiting.")
        sys.exit(1)
 
    device_name=sys.argv[1]
    device=None
    connection_name="CONNECTION"
    connection=None
    config_name="CONFIG_PROCESS"
    config=None

    indiclient.log("LOADING DEVICE CONFIG <%s>" % device_name)

    while not(device):
        device=indiclient.getDevice(device_name)
        time.sleep(0.2)
        if (device):
            indiclient.log("DEVICE READY - device")
     
    while device and \
          not(connection):
        connection=device.getSwitch(connection_name)
        time.sleep(0.2)
        if (connection):
            indiclient.log("SWITCH READY - connection")

    while device and \
          connection and \
          not(device.isConnected()):
        connection[0].s=PyIndi.ISS_ON
        connection[1].s=PyIndi.ISS_OFF
        indiclient.sendNewSwitch(connection)
        time.sleep(0.2)
        if (device.isConnected()):
            indiclient.log("DEVICE CONNECTED / SWITCH ON - device / connection")

    while device and \
          connection and \
          device.isConnected() and \
          not(config):
        config=device.getSwitch(config_name)
        time.sleep(0.2)
        if (config):
            indiclient.log("SWITCH READY - config")

    if device and \
       connection and \
       device.isConnected() and \
       config:
        config[0].s=PyIndi.ISS_ON
        config[1].s=PyIndi.ISS_OFF
        config[2].s=PyIndi.ISS_OFF
        indiclient.sendNewSwitch(config)
        indiclient.log("CONFIG LOADED") 

