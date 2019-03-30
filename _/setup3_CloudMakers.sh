#!/bin/bash

exit

# CloudMakers
pushd ~
[ -d CloudMakers ] && exit 1
mkdir CloudMakers
cd ~/CloudMakers
wget http://download.cloudmakers.eu/atikccd-1.30-armhf.deb
#wget http://download.cloudmakers.eu/atikccd-1.29-armhf.deb
#wget http://download.cloudmakers.eu/shoestring-1.3-armhf.deb
#wget http://download.cloudmakers.eu/usbfocus-0.9-armhf.deb
dpkg -i *.deb
ln -s /usr/local/bin/indi_atik_ccd /usr/bin/indi_atik_ccd
ln -s /usr/local/bin/atik_ccd_test /usr/bin/atik_ccd_test
ln -s /usr/local/bin/indi_atik_wheel /usr/bin/indi_atik_wheel
ln -s /usr/local/share/indi/indi_atik.xml /usr/share/indi/indi_atik.xml

popd
