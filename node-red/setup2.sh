#!/bin/bash
bash <(curl -sL https://raw.githubusercontent.com/node-red/raspbian-deb-package/master/resources/update-nodejs-and-nodered)
apt install -y mosquitto mosquitto-clients libavahi-compat-libdnssd-dev

