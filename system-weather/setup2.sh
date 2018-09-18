#!/bin/bash

# Bus 001 Device 005: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port
[ ! -f /lib/udev/rules.d/99-aagcloudwatcher.rules ] && \
cat > /lib/udev/rules.d/99-aagcloudwatcher.rules <<- EOF
# AAG Cloud Watcher udev rule
SUBSYSTEMS=="usb", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", GROUP="dialout", MODE="0666", SYMLINK+="aagcloudwatcher"
EOF

[ $(grep weather /etc/passwd|wc -l) -eq 0 ] && \

useradd -m -s /bin/bash weather && \
adduser weather dialout && \
adduser weather plugdev && \
adduser weather video && \
adduser weather gpio && \
sed -i 's/^#alias l/alias l/g' /home/weather/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
sed -i 's/ttyUSB0/aagcloudwatcher/' /usr/share/indi/indi_aagcloudwatcher_sk.xml

systemctl daemon-reload
systemctl enable arua_system-weather_indiserver.service
systemctl restart arua_system-weather_indiserver.service

