#!/bin/bash

pushd ~
[ -d ~/indi ] || exit 1
[ -d ~/wiringPi ] || exit 1
[ -d indi_wiringpi_gpio ] || exit 1

[ -f ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ] && mv -f ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ~/indi/libindi/libs/indibase/indidome.cpp
[ -f ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ] && mv -f ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ~/indi/libindi/drivers/dome/dome_script.cpp
[ -f ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL ] && mv -f ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL ~/indi/libindi/drivers/weather/weatherwatcher.cpp

# libindi
# 3rd party
cd ~/indi
git stash 
git pull

# enquanto der erro na rtlsdr - updated libdspau 1.05, 2.0.5 - 09-jan-2019
# revertendo para antes da atualizacao da libdspau - 03-nov-2018
git checkout 8d839b89929926ae253772349246c727e2cc3987 ./3rdparty/indi-rtlsdr/indi_rtlsdr_detector.cpp

# WiringPi
cd ~/wiringPi
git pull

# Indi WiringPi GPIO
cd ~/indi_wiringpi_gpio
git pull

popd
