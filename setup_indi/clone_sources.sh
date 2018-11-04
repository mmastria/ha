#!/bin/bash

pushd ~
[ -d ~/indi ] && exit 1
[ -d ~/wiringPi ]  && exit 1
[ -d indi_wiringpi_gpio ] && exit 1
[ -d CloudMakers ] && exit 1

# libindi
# 3rd party
git clone https://github.com/indilib/indi.git
# WiringPi
git clone git://git.drogon.net/wiringPi
# Indi WiringPi GPIO
git clone https://github.com/magnue/indi_wiringpi_gpio.git
# CloudMakers
mkdir CloudMakers
cd ~/CloudMakers
wget http://download.cloudmakers.eu/atikccd-1.29-armhf.deb
wget http://download.cloudmakers.eu/shoestring-1.3-armhf.deb
wget http://download.cloudmakers.eu/usbfocus-0.9-armhf.deb

popd

