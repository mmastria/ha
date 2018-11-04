#!/bin/bash

pushd ~
[ -d ~/indi ] || exit 1
[ -d ~/wiringPi ] || exit 1
[ -d indi_wiringpi_gpio ] || exit 1

# libindi
# 3rd party
cd ~/indi
git pull

# WiringPi
cd ~/wiringPi
git pull

# Indi WiringPi GPIO
cd ~/indi_wiringpi_gpio
git pull

popd
