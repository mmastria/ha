#!/bin/bash

# -- The following OPTIONAL packages have not been found:

# * OggTheora
# * GTest
# * GMock

# libindi
cd
[ -d ~/indi ] ||  git clone https://github.com/indilib/indi.git
diff -q ~/ha/setup_indi/indidome.cpp.ORIGINAL ~/indi/libindi/libs/indibase/indidome.cpp  && \
cp -f ~/ha/setup_indi/indidome.cpp.NEW ~/indi/libindi/libs/indibase/indidome.cpp 
diff -q ~/ha/setup_indi/dome_script.cpp.ORIGINAL ~/indi/libindi/drivers/dome/dome_script.cpp  && \
cp -f ~/ha/setup_indi/dome_script.cpp.NEW ~/indi/libindi/drivers/dome/dome_script.cpp 
~/indi/libindi/drivers/weather/weatherwatcher.cpp
diff -q ~/ha/setup_indi/weatherwatcher.cpp.ORIGINAL ~/indi/libindi/drivers/weather/weatherwatcher.cpp  && \
cp -f ~/ha/setup_indi/weatherwatcher.cpp.NEW ~/indi/libindi/drivers/weather/weatherwatcher.cpp
diff -q ~/ha/setup_indi/vantage.cpp.ORIGINAL ~/indi/libindi/drivers/weather/vantage.cpp  && \
cp -f ~/ha/setup_indi/vantage.cpp.NEW ~/indi/libindi/drivers/weather/vantage.cpp
mkdir -p ~/indi/buid/libindi
cd ~/indi/buid/libindi/
#cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function" -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/indi/libindi
cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function" -DCMAKE_INSTALL_PREFIX=/usr ~/indi/libindi
make install

# 3rd party
cd ~/indi/3rdparty/
cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function" -DCMAKE_INSTALL_PREFIX=/usr .
make
make install
cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function" -DCMAKE_INSTALL_PREFIX=/usr .
make
make install

# WiringPi
cd
[ -d ~/wiringPi ] || git clone git://git.drogon.net/wiringPi
cd ~/wiringPi/
./build 
echo "/usr/local/lib" | tee /etc/ld.so.conf.d/usr_local_lib.conf
ldconfig

# Indi WiringPi GPIO
cd
[ -d indi_wiringpi_gpio ] || git clone https://github.com/magnue/indi_wiringpi_gpio.git
diff -q ~/ha/setup_indi/wiringpi_gpio.cpp.ORIGINAL ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp && \
cp -f ~/ha/setup_indi/wiringpi_gpio.cpp.NEW ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp
cd ~/indi_wiringpi_gpio
mkdir -p build
cd build
cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function" -DCMAKE_INSTALL_PREFIX=/usr . ..
make install

# CloudMakers
cd
mkdir CloudMakers
cd ~/CloudMakers
wget http://download.cloudmakers.eu/atikccd-1.29-armhf.deb
wget http://download.cloudmakers.eu/shoestring-1.3-armhf.deb
wget http://download.cloudmakers.eu/usbfocus-0.9-armhf.deb
dpkg -i *.deb

# PyIndi
pip install --install-option="--prefix=/usr/local" pyindi-client

# apt -y install indi-full
# apt-get -y install python-rpi.gpio python-requests

