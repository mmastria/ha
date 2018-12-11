#!/bin/bash

# Indi WiringPi GPIO
pushd ~

[ -d indi_wiringpi_gpio ] || exit 1

[ -f ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp.ORIGINAL ] || cp ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp.ORIGINAL

diff -q ~/ha/setup2_indi/wiringpi_gpio.cpp.ORIGINAL ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp.ORIGINAL || exit 1
cp -f ~/ha/setup2_indi/wiringpi_gpio.cpp.NEW ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp

mkdir -p ~/indi_wiringpi_gpio/build
cd ~/indi_wiringpi_gpio/build
# -DCMAKE_BUILD_TYPE=Debug
cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function -Wno-unused-result" -DCMAKE_INSTALL_PREFIX=/usr . ..
make install

popd

