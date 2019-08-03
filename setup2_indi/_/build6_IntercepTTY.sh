#!/bin/bash

# IntercepTTY 
pushd ~

[ -d ~/interceptty ] || exit 1 

cd ~/interceptty/

./configure && \
make && \
make install

popd
