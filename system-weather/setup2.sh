#!/bin/bash

[ $(grep weather /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash weather && \
adduser weather dialout && \
adduser weather plugdev && \
adduser weather video && \
adduser weather gpio && \
sed -i 's/^#alias l/alias l/g' /home/weather/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/

systemctl daemon-reload
systemctl enable arua_system-weather_indiserver.service
systemctl restart arua_system-weather_indiserver.service
