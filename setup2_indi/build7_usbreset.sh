#!/bin/bash

# usbreset 
pushd ~

[ -d ~/usbreset ] || exit 1 

cd ~/usbreset/

cc usbreset.c -o usbreset &&
chmod +x usbreset

popd
