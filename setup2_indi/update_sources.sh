#!/bin/bash

pushd ~
[ -d ~/indi ] || exit 1
[ -d ~/wiringPi ] || exit 1
[ -d indi_wiringpi_gpio ] || exit 1

[ -f ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ] || cp ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ~/indi/libindi/libs/indibase/indidome.cpp
[ -f ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ] || cp ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ~/indi/libindi/drivers/dome/dome_script.cpp
[ -f ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL ] || cp ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL ~/indi/libindi/drivers/weather/weatherwatcher.cpp

# libindi
# 3rd party
cd ~/indi
git stash 
git pull

# WiringPi
cd ~/wiringPi
git pull

# Indi WiringPi GPIO
cd ~/indi_wiringpi_gpio
git pull

popd
