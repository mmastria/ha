#!/bin/bash

# iOptron CEM120
# Atik 320E
# QHY5L-II Mono
# Seletek Armadillo 2 Remote
# Astrometry Remote
# AAG CloudWatcher Remote
# RollOff Roof Remote

[ $(grep west /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash west && \
adduser west dialout && \
adduser west gpio && \
sed -i 's/^#alias l/alias l/g' /home/west/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/

systemctl daemon-reload

systemctl enable arua_system-west_indiserver.service
systemctl restart arua_system-west_indiserver.service
