#!/bin/bash


[ $(grep obs /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash obs && \
adduser obs dialout && \
adduser obs gpio && \
sed -i 's/^#alias l/alias l/g' /home/obs/.bashrc

mkdir /usr/share/indi/scripts
cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
cp -f *.py /usr/share/indi/scripts/

systemctl daemon-reload

systemctl enable arua_system-obs_indiserver.service
systemctl restart arua_system-obs_indiserver.service