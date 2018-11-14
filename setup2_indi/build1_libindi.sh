#!/bin/bash

# -- The following OPTIONAL packages have not been found:

# * OggTheora
# * GTest
# * GMock

# libindi
pushd ~

[ -d ~/indi ] || exit 1 
[ -f ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL ] || cp ~/indi/libindi/libs/indibase/indidome.cpp ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL
[ -f ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL ] || cp ~/indi/libindi/drivers/dome/dome_script.cpp ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL
[ -f ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL ] || cp ~/indi/libindi/drivers/weather/weatherwatcher.cpp ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL

diff -q ~/ha/setup2_indi/indidome.cpp.ORIGINAL ~/indi/libindi/libs/indibase/indidome.cpp.ORIGINAL || exit 1 
diff -q ~/ha/setup2_indi/dome_script.cpp.ORIGINAL ~/indi/libindi/drivers/dome/dome_script.cpp.ORIGINAL || exit 1
diff -q ~/ha/setup2_indi/weatherwatcher.cpp.ORIGINAL ~/indi/libindi/drivers/weather/weatherwatcher.cpp.ORIGINAL || exit 1

cp -f ~/ha/setup2_indi/indidome.cpp.NEW ~/indi/libindi/libs/indibase/indidome.cpp 
cp -f ~/ha/setup2_indi/dome_script.cpp.NEW ~/indi/libindi/drivers/dome/dome_script.cpp 
cp -f ~/ha/setup2_indi/weatherwatcher.cpp.NEW ~/indi/libindi/drivers/weather/weatherwatcher.cpp

mkdir -p ~/indi/build/libindi
cd ~/indi/build/libindi/

# -DCMAKE_BUILD_TYPE=Debug
cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function -Wno-unused-result" -DCMAKE_INSTALL_PREFIX=/usr ~/indi/libindi
make install

popd

