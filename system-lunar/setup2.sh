#!/bin/bash

# iOptron CEM120 / ttyUSB0
# Watec / tty
# QHY5L-II Mono
# Astrometry
# WatchDog
# Moonlite Focuser 
# Weather Meta Remote
# Dome Scripting Gateway Remote 

[ $(grep lunar /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash lunar && \
adduser lunar dialout && \
adduser lunar video && \
adduser lunar gpio && \
sed -i 's/^#alias l/alias l/g' /home/lunar/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
[ ! -d /home/lunar/.indi ] && mkdir -p /home/lunar/.indi && chown lunar:lunar /home/lunar/.indi
cp -f *.default /home/lunar/.indi/
ls -1 /home/lunar/.indi/*.default|xargs -n 1 -I{a} echo {a}|sed 's/.default//'|xargs -r -n 1 -I{b} cp {b}.default {b}
chown lunar:lunar /home/lunar/.indi/*.default
chown lunar:lunar /home/lunar/.indi/*.xml

systemctl daemon-reload

systemctl stop arua_system-west_indiserver.service
systemctl disable arua_system-west_indiserver.service
systemctl enable arua_system-lunar_indiserver.service
systemctl restart arua_system-lunar_indiserver.service
