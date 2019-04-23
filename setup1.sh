#!/bin/bash

#set -x

# etcher raspbian stretch
# touch /boot/ssh

# ssh pi@ip
# sudo passwd root
# su root -
# sed -i '/^#PermitRootLogin/ c\PermitRootLogin Yes' /etc/ssh/sshd_config
# reboot
# ssh root@ip
# raspi-config
# raspi-config - Advanced / Split Memory / GPU = 16
# apt -y install git
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
SSED=$(echo "/raspberrypi/ c127.0.0.1\t$SDEVICE \t$SDEVICE.arua")

raspi-config

# aagsolo
[ "$(mount|grep /dev/root.*\(ro,|wc -l)" == "1" ] && mount -o remount,rw /dev/root /
[ "$(mount|grep /dev/boot.*\(ro,|wc -l)" == "1" ] && mount -o remount,rw /dev/boot /boot

sed -i 's/en_GB.UTF-8/# en_GB.UTF-8/' /etc/locale.gen
sed -i 's/# en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_TYPE=en_US.UTF-8
#export LC_ALL=en_US.UTF-8

locale-gen en_US.UTF-8

dpkg-reconfigure -f noninteractive locales
update-locale en_US.UTF-8

cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
echo "America/Sao_Paulo" > /etc/timezone
#dpkg-reconfigure -f noninteractive tzdata
dpkg-reconfigure tzdata

git config credential.helper store
git config --global user.email "marco@mastria.com.br"
git config --global user.name "mmastria"
git config --global http.postBuffer 524288000
git pull

passwd <<eof
0
0
eof

sed -i '/^#PermitRootLogin/ c\PermitRootLogin Yes' /etc/ssh/sshd_config
sed -i 's/AcceptEnv LANG/#AcceptEnv LANG/' /etc/ssh/sshd_config
systemctl restart ssh

. ./os_update.sh

sed -i $"$SSED" /etc/hosts
echo $SDEVICE > /etc/hostname
sed -i 's/^# export/export/g' /root/.bashrc
sed -i 's/^# eval/eval/g' /root/.bashrc
sed -i 's/^# alias l/alias l/g' /root/.bashrc

apt-get -y install build-essential git python-dev python-pip vim cmake ntpdate \
       cdbs libcfitsio-dev libnova-dev \
       libusb-1.0-0-dev libjpeg-dev libusb-dev libtiff5-dev \
       libftdi1-dev fxload libkrb5-dev libcurl4-gnutls-dev \
       libraw-dev libgphoto2-dev libgsl-dev dkms \
       libboost-regex-dev libgps-dev libdc1394-22-dev \
       zlib1g-dev libffi-dev libfftw3-dev librtlsdr-dev ffmpeg gawk lsof libav-tools libavcodec-dev libavdevice-dev \
       libgtest-dev google-mock oggvideotools \
       astrometry.net \
       screen \
       fswebcam 
       #python-pygame python-pil libsdl1.2-dev
[ '$DEVICE' == 'aagsolo' ] && apt-get -y install swig 
[ '$DEVICE' != 'aagsolo' ] && apt-get -y install swig2.0 libz3-dev raspberrypi-kernel-headers
apt-get -y --fix-broken install
apt-get -y autoremove
apt-get -y clean 
pushd /usr/src/googletest
cmake CMakeLists.txt 
cd /usr/src/gtest
cmake CMakeLists.txt
make
cp *.a /usr/lib
cd /usr/src/gmock
make
cp *.a /usr/lib
popd
[ ! -f /usr/lib/arm-linux-gnueabihf/libnova-0.14.so.0 ] && ln -s /usr/lib/arm-linux-gnueabihf/libnova-0.16.so.0 /usr/lib/arm-linux-gnueabihf/libnova-0.14.so.0
[ ! -f /usr/bin/swig ] && ln -s /usr/bin/swig2.0 /usr/bin/swig
sed -i '/NTPDATE_USE_NTP_CONF/ cNTPDATE_USE_NTP_CONF=no' /etc/default/ntpdate
sed -i '/NTPSERVERS/ cNTPSERVERS="a.st1.ntp.br b.st1.ntp.br c.st1.ntp.br d.st1.ntp.br a.ntp.br b.ntp.br c.ntp.br gps.ntp.br"' /etc/default/ntpdate
[ '$DEVICE' != 'aagsolo' ] && timedatectl set-ntp true

[ ! -f /usr/bin/zram.sh ] && \
cp -f zram.sh /usr/bin/ && \
sed -i '$i/usr/bin/zram.sh &' /etc/rc.local

# enable hardware serial for system-env
sed -i 's/console=serial0,115200 //' /boot/cmdline.txt
echo "##############################" >> /boot/config.txt
echo "# enabling UART to GPIO Serial" >> /boot/config.txt
echo "#" >> /boot/config.txt
echo "enable_uart=1" >> /boot/config.txt
echo "dtoverlay=pi3-disable-bt" >> /boot/config.txt
echo "#" >> /boot/config.txt
echo "##############################" >> /boot/config.txt
systemctl stop serial-getty@ttyAMA0.service
systemctl disable serial-getty@ttyAMA0.service
systemctl stop serial-getty@ttyS0.service
systemctl disable serial-getty@ttyS0.service
systemctl stop hciuart
systemctl disable hciuart

read -p "key to reboot"
reboot


# apt -y install indi-full
# apt-get -y install python-rpi.gpio python-requests

