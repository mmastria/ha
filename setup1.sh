#!/bin/bash

# etcher raspibian stretch
# touch /boot/ssh

# sudo raspi-config

# sudo su -
# apt update && apt -y install git
# git clone https://github.com/mmastria/ha.git
# cd ha
# ./setup1.sh

# doc
# http://www.clearskyinstitute.com/INDI/INDI.pdf

# dev
# https://github.com/indilib/indi

# PyIndi
# http://indilib.org/support/tutorials/166-installing-and-using-the-python-pyndi-client-on-raspberry-pi.html

# verificar
# pi config - http://baddotrobot.com/blog/2017/03/01/standard-pi-setup/
# telescope scripts - https://github.com/indilib/indi/blob/master/libindi/drivers/telescope/telescope_script.txt
# indi python ex - https://github.com/HazenBabcock/indi-python/tree/master/indi_python
# indi python ex - http://indilib.org/develop/tutorials/151-time-lapse-astrophotography-with-indi-python.html

if [ $# -eq 0 -o ! -d "$1" ];then echo -e "$0 <system-xxxx>";exit 1;fi
SDEVICE="${1///}"
SSED=$(echo "/raspberrypi/ c127.0.0.1\t$SDEVICE \t$SDEVICE.local")

sed -i 's/en_GB.UTF-8/# en_GB.UTF-8/' /etc/locale.gen
sed -i 's/# en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen
locale-gen

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_TYPE=en_US.UTF-8

dpkg-reconfigure -f noninteractive locales

cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
echo "America/Sao_Paulo" > /etc/timezone
#dpkg-reconfigure -f noninteractive tzdata
dpkg-reconfigure tzdata

git config credential.helper store
git config --global user.email "marco@mastria.com.br"
git pull

passwd <<eof
0
0
eof

sed -i '/^#PermitRootLogin/ c\PermitRootLogin Yes' /etc/ssh/sshd_config
sed -i 's/AcceptEnv LANG/#AcceptEnv LANG/' /etc/ssh/sshd_config
#systemctl enable ssh
systemctl restart ssh

. ./os_update.sh

sed -i $"$SSED" /etc/hosts
echo $SDEVICE > /etc/hostname
sed -i 's/^# export/export/g' /root/.bashrc
sed -i 's/^# eval/eval/g' /root/.bashrc
sed -i 's/^# alias l/alias l/g' /root/.bashrc

apt -y install build-essential git python-dev python-pip vim ntpdate \
       cdbs libcfitsio-dev libnova-dev \
       libusb-1.0-0-dev libjpeg-dev libusb-dev libtiff5-dev \
       libftdi1-dev fxload libkrb5-dev libcurl4-gnutls-dev \
       libraw-dev libgphoto2-dev libgsl-dev dkms \
       libboost-regex-dev libgps-dev libdc1394-22-dev \
       swig2.0 libz3-dev zlib1g-dev
apt -y --fix-broken install
ln -s /usr/bin/swig2.0 /usr/bin/swig
ln -s /usr/lib/arm-linux-gnueabihf/libnova-0.16.so.0 /usr/lib/arm-linux-gnueabihf/libnova-0.14.so.0
sed '/NTPSERVERS/ cNTPSERVERS="a.st1.ntp.br b.st1.ntp.br c.st1.ntp.br d.st1.ntp.br a.ntp.br b.ntp.br c.ntp.br gps.ntp.br"' /etc/default/ntpdate

# apt -y install indi-full
# pip2 install --upgrade pip

. ./libindi_update.sh

pip install --install-option="--prefix=/usr/local" pyindi-client 

read -p "key to reboot"
reboot
