#!/bin/bash

# run as root to use socat

./rtl-sdr-rules.sh
sed -i 's/^#alias l/alias l/g' /root/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
cp -f *.py /usr/local/bin/
cp -f *sk.xml /usr/share/indi/
[ ! -d /root/.indi ] && mkdir -p /root/.indi
cp -f *.default /root/.indi/
ls -1 /root/.indi/*.default|xargs -n 1 -I{a} echo {a}|sed 's/.default//'|xargs -r -n 1 -I{b} cp {b}.default {b}
mkdir -p ~/images

systemctl daemon-reload

systemctl enable arua_cloudWatcherMux.service
systemctl restart arua_cloudWatcherMux.service

systemctl enable arua_allsky.service
systemctl restart arua_allsky.service

systemctl enable arua_system-env_indiserver.service
systemctl restart arua_system-env_indiserver.service
