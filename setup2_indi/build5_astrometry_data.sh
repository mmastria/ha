#!/bin/bash

# Astrometry Data
pushd ~

[ -d astrometry_data ] || exit 1

mkdir -p ~/astrometry_data
cd ~/astrometry_data

curl http://data.astrometry.net/debian/astrometry-data-4208-4219_0.45_all.deb -o astrometry-data-4208-4219_0.45_all.deb
curl http://data.astrometry.net/debian/astrometry-data-4207_0.45_all.deb -o astrometry-data-4207_0.45_all.deb
curl http://data.astrometry.net/debian/astrometry-data-4206_0.45_all.deb -o astrometry-data-4206_0.45_all.deb
curl http://data.astrometry.net/debian/astrometry-data-4205_0.45_all.deb -o astrometry-data-4205_0.45_all.deb
curl http://data.astrometry.net/debian/astrometry-data-4204_0.45_all.deb -o astrometry-data-4204_0.45_all.deb
curl http://data.astrometry.net/debian/astrometry-data-4203_0.45_all.deb -o astrometry-data-4203_0.45_all.deb

dpkg -i *.deb

popd

