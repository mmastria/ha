#!/bin/bash
pushd .node-red
npm uninstall node-red-contrib-sonoff-tasmota
npm install https://github.com/mmastria/node-red-contrib-sonoff-tasmota
popd

