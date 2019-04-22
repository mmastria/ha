#!/bin/bash

# run as root to use socat

# necessario para camera USB DVC100
#rmmod em28xx
#modprobe em28xx nodrop=1 timeout=5000 quirks=0x80

# resolver como colocar 1vez
#pip install bottle && \
#pip install -U 'gevent~=1.2.2' && \
#pip install multiprocessing && \
#pip install requests && \
#pip install cffi
#./rtl-sdr-rules.sh
#sed -i 's/^#alias l/alias l/g' /root/.bashrc

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
[ ! -d /usr/share/indi/scripts ] && mkdir -p /usr/share/indi/scripts
cp -f ../common/*.py /usr/share/indi/scripts/
cp -f *sk.xml /usr/share/indi/
[ ! -d /root/.indi ] && mkdir -p /root/.indi
cp -f *.default /root/.indi/
ls -1 /root/.indi/*.default|xargs -n 1 -I{a} echo {a}|sed 's/.default//'|xargs -r -n 1 -I{b} cp {b}.default {b}
cp -f allsky_rotate /etc/cron.daily

systemctl daemon-reload

systemctl enable arua_cloudWatcherMux.service
systemctl restart arua_cloudWatcherMux.service

systemctl enable arua_envSafe.service
systemctl restart arua_envSafe.service

systemctl enable arua_allsky.service
systemctl restart arua_allsky.service

systemctl enable arua_system-env_indiserver.service
systemctl restart arua_system-env_indiserver.service
