#!/bin/sh
sudo su -
systemctl enable ssh
passwd <<eof
0
0
eof
sed '/^PermitRootLogin/ c\PermitRootLogin Yes' /etc/ssh/sshd_config
systemctl enable sshd
systemctl restart sshd
apt update
apt -y upgrade
apt -y dist-upgrade
rpi-update
apt -y install vim git
sed '/raspberrypi/ c\127.0.0.1 %1 %1.local' /etc/hosts
echo %1 > /etc/hostname
git clone https://github.com/mmastria/ha.git
cd ha
git config credential.helper store
git config --global user.email "marco@mastria.com.br"
git pull
read -p "key to reboot"
reboot


