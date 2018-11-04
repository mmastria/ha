#!/bin/bash

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
popd

/usr/local to /usr for bin/indi_atik_ccd, bin/indi_atik_wheel and share/indi_atik.xml.
root@system-east:~/ha# whereis indi_atik_ccd
indi_atik_ccd: /usr/local/bin/indi_atik_ccd
root@system-east:~/ha# whereis indi_v4l2_ccd
indi_v4l2_ccd: /usr/bin/indi_v4l2_ccd
root@system-east:~/ha# whereis indi_atik_wheel
indi_atik_wheel: /usr/local/bin/indi_atik_wheel

ln -s /usr/local/bin/indi_atik_ccd /usr/bin/indi_atik_ccd
ln -s /usr/local/bin/atik_ccd_test /usr/bin/atik_ccd_test
ln -s /usr/local/bin/indi_atik_wheel /usr/bin/indi_atik_wheel
ln -s /usr/local/share/indi/indi_atik.xml /usr/share/indi/indi_atik.xml

