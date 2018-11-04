#!/bin/bash

# CloudMakers
pushd ~
[ -d ~/CloudMakers ] || exit 1 
cd ~/CloudMakers
dpkg -i *.deb
popd

# PyIndi
pip install --install-option="--prefix=/usr/local" pyindi-client

# apt -y install indi-full
# apt-get -y install python-rpi.gpio python-requests

