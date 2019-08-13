#!/bin/bash
node-red-stop
pushd .node-red
npm uninstall node-red-contrib-sonoff-tasmota
npm install https://github.com/mmastria/node-red-contrib-sonoff-tasmota
popd
systemctl start nodered.service
