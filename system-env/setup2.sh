#!/bin/bash

# first time only

[ $(grep env /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash env && \
adduser env dialout && \
adduser env video && \
adduser env gpio && \
mkdir /usr/share/indi/scripts && \
pip install bottle && \
pip install -U 'gevent~=1.2.2' && \
pip install multiprocessing && \
pip install requests && \
./rtl-sdr-rules.sh && \
sed -i 's/^#alias l/alias l/g' /home/env/.bashrc

# every execution

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
[ ! -d /usr/share/indi/scripts ] && mkdir -p /usr/share/indi/scripts
cp -f *.py /usr/share/indi/scripts/
[ ! -d /home/env/.indi ] && mkdir -p /home/env/.indi && chown env:env /home/env/.indi
cp -f *.default /home/env/.indi/
ls -1 /home/env/.indi/*.default|xargs -n 1 -I{a} echo {a}|sed 's/.default//'|xargs -r -n 1 -I{b} cp {b}.default {b}
chown env:env /home/env/.indi/*.default
chown env:env /home/env/.indi/*.xml

systemctl daemon-reload

systemctl enable arua_system-env_indiserver.service
systemctl restart arua_system-env_indiserver.service
