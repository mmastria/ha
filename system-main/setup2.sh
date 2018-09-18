#!/bin/bash

[ $(grep weather /etc/passwd|wc -l) -eq 0 ] && \
apt -y install v4l-util &&
useradd -m -s /bin/bash main && \
adduser main dialout && \
adduser main plugdev && \
adduser main video && \
adduser main gpio && \
sed -i 's/^#alias l/alias l/g' /home/main/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/

systemctl daemon-reload
systemctl enable arua_system-main_indiserver.service
systemctl restart arua_system-main_indiserver.service
