#!/bin/bash

# Bus 001 Device 005: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port
[ ! -f /lib/udev/rules.d/99-aagcloudwatcher.rules ] && \
cat > /lib/udev/rules.d/99-aagcloudwatcher.rules <<- EOF
# AAG Cloud Watcher udev rule
SUBSYSTEMS=="usb", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", GROUP="dialout", MODE="0666", SYMLINK+="aagcloudwatcher"
EOF

sed -i 's/ttyUSB0/aagcloudwatcher/' /usr/share/indi/indi_aagcloudwatcher_sk.xml

