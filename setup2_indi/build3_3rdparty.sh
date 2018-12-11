#!/bin/bash

pushd ~

[ -d ~/indi ] || exit 1 

# 3rd party
cd ~/indi/3rdparty/

# -DCMAKE_BUILD_TYPE=Debug
cmake -DCMAKE_CXX_FLAGS="-Wno-psabi -Wno-unused-parameter -Wno-unused-variable -Wno-unused-but-set-parameter -Wno-sign-compare -Wno-reorder -Wno-unused-value -Wno-sign-compare -Wno-misleading-indentation -Wno-maybe-uninitialized -Wno-unused-function -Wno-unused-result" -DCMAKE_INSTALL_PREFIX=/usr .
make
make install

popd

