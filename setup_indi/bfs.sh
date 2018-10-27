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
diff -q ~/ha/setup_indi/weatherwatcher.cpp.ORIGINAL ~/indi/libindi/drivers/weather/weatherwatcher.cpp  && \
cp -f ~/ha/setup_indi/weatherwatcher.cpp.NEW ~/indi/libindi/drivers/weather/weatherwatcher.cpp
diff -q ~/ha/setup_indi/vantage.cpp.ORIGINAL ~/indi/libindi/drivers/weather/vantage.cpp  && \
cp -f ~/ha/setup_indi/vantage.cpp.NEW ~/indi/libindi/drivers/weather/vantage.cpp
mkdir -p ~/indi/buid/libindi
cd ~/indi/buid/libindi/
#cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function" -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/indi/libindi
cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function" -DCMAKE_INSTALL_PREFIX=/usr ~/indi/libindi
make install


