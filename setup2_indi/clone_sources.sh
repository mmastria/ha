#!/bin/bash

pushd ~

# libindi
[ -d ~/indi ] || \
git clone https://github.com/indilib/indi.git

# 3rd party
[ -d ~/indi-3rdparty ] || \
git clone https://github.com/indilib/indi-3rdparty.git

# WiringPi
#[ -d ~/wiringPi ] || \
#git clone git://git.drogon.net/wiringPi

# Indi WiringPi GPIO
#[ -d ~/indi_wiringpi_gpio ] || \
#git clone https://github.com/magnue/indi_wiringpi_gpio.git

# IntercepTTY
#[ -d ~/interceptty ] || \
#git clone https://github.com/geoffmeyers/interceptty.git

# USB Reset
[ -d ~/usbreset ] || \
git clone https://gist.github.com/5124616.git usbreset

popd

