#!/bin/bash

# iOptron CEM60 / ttyUSB1
# Atik 383L+
# Starlight Xpress Filter Wheel
# QHY5L-II Mono
# Astrometry 
# WatchDog
# Seletek Armadillo 2 / ttyUSB0
# Weather Meta Remote
# Dome Scripting Gateway Remote

[ $(grep east /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash east && \
adduser east dialout && \
adduser east video && \
adduser east gpio && \
sed -i 's/^#alias l/alias l/g' /home/east/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
[ ! -d /usr/share/indi/scripts ] && mkdir -p /usr/share/indi/scripts
cp -f ../common/*.py /usr/share/indi/scripts/
[ ! -d /home/east/.indi ] && mkdir -p /home/east/.indi && chown east:east /home/east/.indi
cp -f *.default /home/east/.indi/
ls -1 /home/east/.indi/*.default|xargs -n 1 -I{a} echo {a}|sed 's/.default//'|xargs -r -n 1 -I{b} cp {b}.default {b}
chown east:east /home/east/.indi/*.default
chown east:east /home/east/.indi/*.xml

systemctl daemon-reload

systemctl enable arua_system-east_indiserver.service
systemctl restart arua_system-east_indiserver.service

systemctl enable arua_indi_rest.service
systemctl restart arua_indi_rest.service

