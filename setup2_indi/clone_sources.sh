#!/bin/bash

pushd ~

# libindi
# 3rd party
[ -d ~/indi ] || \
git clone https://github.com/indilib/indi.git

# WiringPi
[ -d ~/wiringPi ] || \
git clone git://git.drogon.net/wiringPi

# Indi WiringPi GPIO
[ -d ~/indi_wiringpi_gpio ] || \
git clone https://github.com/magnue/indi_wiringpi_gpio.git

# IntercepTTY
[ -d ~/interceptty ] || \
git clone https://github.com/geoffmeyers/interceptty.git

popd

