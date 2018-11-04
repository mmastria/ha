#!/bin/bash

pushd ~
[ -d ~/indi ] || exit 1
[ -d ~/wiringPi ] || exit 1
[ -d indi_wiringpi_gpio ] || exit 1
[ -d CloudMakers ] || exit 1

# libindi
# 3rd party
cd indi
git pull
cd
# WiringPi
cd wiringPi
git pull
cd
# Indi WiringPi GPIO
cd indi_wiringpi_gpio
git pull
cd
# CloudMakers
cd ~/CloudMakers
mv atikccd-1.29-armhf.deb atikccd-1.29-armhf.deb.OLD
wget http://download.cloudmakers.eu/atikccd-1.29-armhf.deb
mv shoestring-1.3-armhf.deb shoestring-1.3-armhf.deb.OLD 
wget http://download.cloudmakers.eu/shoestring-1.3-armhf.deb
mv usbfocus-0.9-armhf.deb usbfocus-0.9-armhf.deb.OLD
wget http://download.cloudmakers.eu/usbfocus-0.9-armhf.deb
cd

popd
