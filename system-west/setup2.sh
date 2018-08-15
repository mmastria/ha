#!/bin/bash

# iOptron CEM120
# Atik 314L+
# QHY5L-II Mono
# Seletek Armadillo 2 Remote
# Astrometry Remote
# AAG CloudWatcher Remote
# RollOff Roof Remote

[ $(grep west /etc/passwd|wc -l) -eq 0 ] && \
useradd -m west && \
adduser west dialout && \
adduser west gpio

cp -f *.service /etc/systemd/system/
cp -f *.sh /usr/local/bin/

systemctl daemon-reload

systemctl enable arua_system-west_indiserver.service
systemctl enable arua_cem120.service
systemctl enable arua_qhy5lii.service
systemctl enable arua_atik320e.service

systemctl restart arua_system-west_indiserver.service
systemctl restart arua_cem120.service
systemctl restart arua_qhy5lii.service
systemctl restart arua_atik320e.service
