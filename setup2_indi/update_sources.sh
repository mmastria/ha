#!/bin/bash

pushd ~
[ -d ~/indi ] || exit 1
[ -d ~/wiringPi ] || exit 1
[ -d ~/indi_wiringpi_gpio ] || exit 1
[ -d ~/interceptty ] || exit 1

[ -f ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ] && mv -f ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ~/indi/libindi/libs/indibase/indidome.cpp
[ -f ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ] && mv -f ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ~/indi/libindi/drivers/dome/dome_script.cpp
[ -f ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL ] && mv -f ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL ~/indi/libindi/drivers/weather/weatherwatcher.cpp

[ -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp.ORIGINAL ] && mv -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp.ORIGINAL ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp
[ -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h.ORIGINAL ] && mv -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h.ORIGINAL ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h

[ -f ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp.ORIGINAL ] && mv -f ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp.ORIGINAL ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp

# libindi
# 3rd party
cd ~/indi
git stash 
git pull

# enquanto der erro na rtlsdr - updated libdspau 1.05, 2.0.5 - 09-jan-2019
# revertendo para antes da atualizacao da libdspau - 03-nov-2018
##git checkout 8d839b89929926ae253772349246c727e2cc3987 ./3rdparty/indi-rtlsdr/indi_rtlsdr_detector.cpp
##git checkout 8d839b89929926ae253772349246c727e2cc3987 ./3rdparty/indi-rtlsdr/indi_rtlsdr_detector.cpp
# erro em indi-radiosim
##git checkout f8b50d4257361517cb6234f748dc8939151f0a1f ./3rdparty/indi-radiosim/indi_radiosim_detector.cpp

# WiringPi
cd ~/wiringPi
git pull

# Indi WiringPi GPIO
cd ~/indi_wiringpi_gpio
git pull

# IntercepTTY 
cd ~/interceptty
git pull

popd
