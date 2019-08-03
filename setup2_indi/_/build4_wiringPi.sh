#!/bin/bash

# WiringPi
pushd ~

[ -d ~/wiringPi ] || exit 1 

cd ~/wiringPi/
# -Wunused-function
./build 
echo "/usr/local/lib" | tee /etc/ld.so.conf.d/usr_local_lib.conf
ldconfig

popd
