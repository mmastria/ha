#!/bin/bash

pushd ~
[ -d ~/indi ] || exit 1
[ -d ~/indi-3rdparty ] || exit 1
#[ -d ~/wiringPi ] || exit 1
#[ -d ~/indi_wiringpi_gpio ] || exit 1
#[ -d ~/interceptty ] || exit 1
[ -d ~/usbreset ] || exit 1

#[ -f ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ] && mv -f ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ~/indi/libindi/libs/indibase/indidome.cpp
#[ -f ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ] && mv -f ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ~/indi/libindi/drivers/dome/dome_script.cpp

#[ -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp.ORIGINAL ] && mv -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp.ORIGINAL ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp
#[ -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h.ORIGINAL ] && mv -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h.ORIGINAL ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h

#[ -f ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp.ORIGINAL ] && mv -f ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp.ORIGINAL ~/indi_wiringpi_gpio/wiringpi_gpio/wiringpi_gpio.cpp

# libindi
cd ~/indi

# --------
#rm -f libindi/drivers/weather/weatherwatcher.cpp
#git checkout libindi/drivers/weather/weatherwatcher.cpp
#git stash 
# --------
git pull
# --------
## TEMP
#sed -i '0,/keywordT\[1\]/{s/minOK = -10/minOK = -20/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[1\]/{s/maxOK = 30/maxOK = 1/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[1\]/{s/percWarn = 15/percWarn = 0/}' libindi/drivers/weather/weatherwatcher.cpp
## WIND
#sed -i '0,/keywordT\[2\]/{s/minOK = 0/minOK = -1/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[2\]/{s/maxOK = 20/maxOK = -1/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[2\]/{s/percWarn = 15/percWarn = 0/}' libindi/drivers/weather/weatherwatcher.cpp
## GUST
#sed -i '0,/keywordT\[3\]/{s/minOK = 0/minOK = -1/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[3\]/{s/maxOK = 20/maxOK = -1/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[3\]/{s/percWarn = 15/percWarn = 0/}' libindi/drivers/weather/weatherwatcher.cpp
## RAIN 
#sed -i '0,/keywordT\[0\]/{s/minOK = 0/minOK = 2400/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[0\]/{s/maxOK = 0/maxOK = 2700/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[0\]/{s/percWarn = 15/percWarn = 5/}' libindi/drivers/weather/weatherwatcher.cpp
## FORECAST 
#sed -i '0,/keywordT\[4\]/{s/minOK = 0/minOK = 0/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[4\]/{s/maxOK = 0/maxOK = 1/}' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '0,/keywordT\[4\]/{s/percWarn = 15/percWarn = 0/}' libindi/drivers/weather/weatherwatcher.cpp

## TEMP
#sed -i '/keywordT\[1\]/,/minOK/s/-10/-20/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[1\]/,/maxOK/s/30/1/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[1\]/,/percWarn/s/15/0/' libindi/drivers/weather/weatherwatcher.cpp
## WIND
#sed -i '/keywordT\[2\]/,/minOK/s/0/-1/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[2\]/,/maxOK/s/20/-1/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[2\]/,/percWarn/s/15/0/' libindi/drivers/weather/weatherwatcher.cpp
## GUST
#sed -i '/keywordT\[3\]/,/minOK/s/0/-1/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[3\]/,/maxOK/s/20/-1/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[3\]/,/percWarn/s/15/0/' libindi/drivers/weather/weatherwatcher.cpp
## RAIN 
#sed -i '/keywordT\[0\]/,/minOK/s/0/2400/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[0\]/,/maxOK/s/0/2700/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[0\]/,/percWarn/s/15/5/' libindi/drivers/weather/weatherwatcher.cpp
## FORECAST 
#sed -i '/keywordT\[4\]/,/minOK/s/0/0/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[4\]/,/maxOK/s/0/1/' libindi/drivers/weather/weatherwatcher.cpp
#sed -i '/keywordT\[4\]/,/percWarn/s/15/0/' libindi/drivers/weather/weatherwatcher.cpp
# --------

# enquanto der erro na rtlsdr - updated libdspau 1.05, 2.0.5 - 09-jan-2019
# revertendo para antes da atualizacao da libdspau - 03-nov-2018
##git checkout 8d839b89929926ae253772349246c727e2cc3987 ./3rdparty/indi-rtlsdr/indi_rtlsdr_detector.cpp
##git checkout 8d839b89929926ae253772349246c727e2cc3987 ./3rdparty/indi-rtlsdr/indi_rtlsdr_detector.cpp
# erro em indi-radiosim
##git checkout f8b50d4257361517cb6234f748dc8939151f0a1f ./3rdparty/indi-radiosim/indi_radiosim_detector.cpp

# 3rd party
cd ~/indi-3rdparty
git pull

# WiringPi
#cd ~/wiringPi
#git pull

# Indi WiringPi GPIO
#cd ~/indi_wiringpi_gpio
#git pull

# IntercepTTY 
#cd ~/interceptty
#git pull

# usbreset
cd ~/usbreset
git pull

popd
