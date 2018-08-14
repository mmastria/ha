#!/bin/sh

# sudo su -
# apt update && apt -y install git
# git clone https://github.com/mmastria/ha.git
# cd ha
# ./setup1.sh

git config credential.helper store
git config --global user.email "marco@mastria.com.br"
git pull

passwd <<eof
0
0
eof

sed -i '/^PermitRootLogin/ c\PermitRootLogin Yes' /etc/ssh/sshd_config
systemctl enable ssh
systemctl restart ssh

apt -y upgrade
apt -y dist-upgrade
rpi-update

apt -y install cdbs libcfitsio-dev libnova-dev libusb-1.0-0-dev libjpeg-dev libusb-dev libtiff5-dev libftdi1-dev fxload libkrb5-dev libcurl4-gnutls-dev libraw-dev libgphoto2-dev libgsl-dev dkms libboost-regex-dev libgps-dev libdc1394-22-dev wget

# wget http://indilib.org/download/send/6-raspberry-pi/9-indi-library-for-raspberry-pi.html
wget http://indilib.org/download/raspberry-pi/send/6-raspberry-pi/9-indi-library-for-raspberry-pi.html

tar -xzf libindi_1.7.3_rpi.tar.gz
cd libindi_1.7.3_rpi
dpkg -i *.deb

sed -i '/raspberrypi/ c\127.0.0.1 %1 %1.local' /etc/hosts
echo %1 > /etc/hostname
sed -i 's/^# export/export/g' /root/.bashrc
sed -i 's/^# eval/eval/g' /root/.bashrc
sed -i 's/^# alias l/alias l/g' /root/.bashrc



read -p "key to reboot"
reboot



