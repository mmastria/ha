#!/bin/bash

# iOptron CEM120
# Atik 320E
# QHY5L-II Mono
# Astrometry
# WatchDog
# Seletek Armadillo 2 Remote
# Weather Meta Remote
# Dome Scripting Gateway Remote 

[ $(grep west /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash west && \
adduser west dialout && \
adduser west gpio && \
sed -i 's/^#alias l/alias l/g' /home/west/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
[ ! -d /home/west/.indi ] && mkdir -p /home/west/.indi && chown west:west /home/west/.indi
cp -f *.default /home/west/.indi/
ls -1 /home/west/.indi/*.default|xargs -n 1 -I{a} echo {a}|sed 's/.default//'|xargs -r -n 1 -I{b} cp {b}.default {b}
chown west:west /home/west/.indi/*.default
chown west:west /home/west/.indi/*.xml

systemctl daemon-reload

systemctl enable arua_system-west_indiserver.service
systemctl restart arua_system-west_indiserver.service
