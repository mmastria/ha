#!/bin/bash

# iOptron CEM60
# Atik  383L+
# Starlight Xpress Filter Wheel
# QHY5L-II Mono
# Seletek Armadillo 2 Remote
# Astrometry Remote
# AAG CloudWatcher Remote
# RollOff Roof Remote

[ $(grep east /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash east && \
adduser east dialout && \
adduser east gpio && \
sed -i 's/^#alias l/alias l/g' /home/east/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/

systemctl daemon-reload
systemctl enable arua_system-east_indiserver.service
systemctl restart arua_system-east_indiserver.service
