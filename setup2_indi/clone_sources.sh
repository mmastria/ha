#!/bin/bash

pushd ~
[ -d ~/indi ] && exit 1
[ -d ~/wiringPi ]  && exit 1
[ -d indi_wiringpi_gpio ] && exit 1

# libindi
# 3rd party
git clone https://github.com/indilib/indi.git

# WiringPi
git clone git://git.drogon.net/wiringPi

# Indi WiringPi GPIO
git clone https://github.com/magnue/indi_wiringpi_gpio.git

popd

