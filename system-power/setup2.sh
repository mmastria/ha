#!/bin/bash

# Arduino Power
# Arduino RolllOffRoof
# RollOffRoof Monitor

[ $(grep powerhub /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash powerhub && \
adduser powerhub dialout && \
adduser powerhub gpio && \
sed -i 's/^#alias l/alias l/g' /home/powerhub/.bashrc

[ $(grep rolloffroof /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash rolloffroof && \
adduser rolloffroof dialout && \
adduser rolloffroof gpio && \
sed -i 's/^#alias l/alias l/g' /home/rolloffroof/.bashrc

#
# pyindi-client
#
# login as: rolloffroof
# pip2  install --user --install-option="--prefix=/usr/local" pyindi-client

cp -f *.service /etc/systemd/system/
cp -f *.xml /usr/share/indi/
cp -f *.py /usr/local/bin/
cp -f arua*.sh /usr/local/bin/

systemctl daemon-reload

systemctl enable arua_powerhub_indiserver.service
systemctl enable arua_rolloffroof_indiserver.service
systemctl enable arua_rolloffroof_monitor.service

systemctl restart arua_powerhub_indiserver.service
systemctl restart arua_rolloffroof_indiserver.service
systemctl restart arua_rolloffroof_monitor.service
