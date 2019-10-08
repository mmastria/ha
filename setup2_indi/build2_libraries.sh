#!/bin/bash

#LIBS="libapogee libfishcamp libfli libqhy libqsi libsbig libatik"

pushd ~

#[ -d ~/indi ] || exit 1 
[ -d ~/indi-3rdparty ] || exit 1 

# 3rd party / libraries
#for lib in $LIBS ; do
#(
#  echo "Building $lib ..."
#  mkdir -p ~/indi/3rdparty/build_$lib
#  cd ~/indi/3rdparty/build_$lib
#  # -DCMAKE_BUILD_TYPE=Debug
#  cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function -Wno-unused-result" -DCMAKE_INSTALL_PREFIX=/usr . ../$lib
#  make
#  make install
#)
#done

mkdir -p ~/build/indi-3rdparty-libs
cd ~/build/indi-3rdparty-libs
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug -DBUILD_LIBS=1 ~/indi-3rdparty
make -j4
sudo make install

popd

