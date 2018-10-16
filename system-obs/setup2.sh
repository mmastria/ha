#!/bin/bash


[ $(grep obs /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash obs && \
adduser obs dialout && \
adduser obs video && \
adduser obs gpio && \
mkdir /usr/share/indi/scripts && \
pip install bottle && \
pip install -U 'gevent~=1.2.2' && \
pip install multiprocessing && \
sed -i 's/^#alias l/alias l/g' /home/obs/.bashrc

(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/curl http://192.168.0.205/cgi-bin/cgiLastData -o /tmp/aagsolo.txt") | crontab -


cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
cp -f *.py /usr/share/indi/scripts/

systemctl daemon-reload

systemctl enable arua_system-obs_ror.service
systemctl restart arua_system-obs_ror.service

systemctl enable arua_system-obs_indiserver.service
systemctl restart arua_system-obs_indiserver.service
