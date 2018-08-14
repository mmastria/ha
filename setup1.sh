#!/bin/sh

# sudo su -
# apt update && apt -y install git
# git clone https://github.com/mmastria/ha.git
# cd ha
# ./setup1.sh

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
sed -i '/raspberrypi/ c\127.0.0.1 %1 %1.local' /etc/hosts
echo %1 > /etc/hostname
sed -i 's/^# export/export/g' /root/.bashrc
sed -i 's/^# eval/eval/g' /root/.bashrc
sed -i 's/^# alias l/alias l/g' /root/.bashrc
cd ha
git config credential.helper store
git config --global user.email "marco@mastria.com.br"
git pull
read -p "key to reboot"
reboot


