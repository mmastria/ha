#!/bin/bash

pushd ~

[ -d ~/indi-3rdparty ] || exit 1 

#[ -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp.ORIGINAL ] || cp ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp.ORIGINAL
#[ -f ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h.ORIGINAL ] || cp ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h.ORIGINAL

#diff -q ~/ha/setup2_indi/arm_plat_focuser_common.cpp.ORIGINAL ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp.ORIGINAL || exit 1
#diff -q ~/ha/setup2_indi/arm_plat_focuser_common.h.ORIGINAL ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h.ORIGINAL || exit 1

#cp -f ~/ha/setup2_indi/arm_plat_focuser_common.cpp.NEW ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.cpp
#cp -f ~/ha/setup2_indi/arm_plat_focuser_common.h.NEW ~/indi/3rdparty/indi-armadillo-platypus/arm_plat_focuser_common.h

# 3rd party
#cd ~/indi/3rdparty/

# -DCMAKE_BUILD_TYPE=Debug
#cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function -Wno-unused-result" -DCMAKE_INSTALL_PREFIX=/usr .
#make
#make install

mkdir -p ~/build/indi-3rdparty
cd ~/build/indi-3rdparty
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/indi-3rdparty
make -j4
sudo make install

popd

