#!/bin/bash

# -DCMAKE_BUILD_TYPE=Debug
#cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function -Wno-unused-result" -DCMAKE_INSTALL_PREFIX=/usr .

pushd ~

[ -d ~/indi ] || exit 1 

# build libatik
cd ~/indi/3rdparty/
mkdir -p build_libatik
cd build_libatik
cmake -DCMAKE_INSTALL_PREFIX=/usr . ../libatik
make
make install

# build driver
cd ~/indi/3rdparty/indi-atik/
mkdir -p build 
cd build 
cmake -DCMAKE_INSTALL_PREFIX=/usr .. 
make 
make install

popd
