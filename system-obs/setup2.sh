#!/bin/bash

# Exclusivo WiringPi GPIO
#
# PWR_RL1C		GPIO17  WPI PIN 0 O
# PWR_RL1B		GPIO18  WPI PIN 1 O
# PWR_RPI/2B		GPIO27  WPI PIN 2 O
# PWR_SCOPE/3B		GPIO22  WPI PIN 3 O
# PWR_MAIN/4B		GPIO23  WPI PIN 4 O
# PWR_RL2C		GPIO4	WPI PIN 7 O
# AAGSAFE		GPIO09	WPI PIN 13 I

# Exlusivo Dome Scripting Gateway
#
# ROR_MOVE/2A		GPIO24	WPI PIN 5  O
# ROR_SWITCH_OPEN	GPIO25	WPI PIN 6  I
# ROR_MOUNT_PARKED	GPIO08	WPI PIN 10 I
# ROR_PARKED/1A		GPIO10	WPI PIN 12 O
# ROR_SW_CLOSED		GPIO11	WPI PIN 14 I


# first time only

[ $(grep obs /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash obs && \
adduser obs dialout && \
adduser obs video && \
adduser obs gpio && \
mkdir /usr/share/indi/scripts && \
pip install bottle && \
pip install -U 'gevent~=1.2.2' && \
pip install multiprocessing && \
pip install requests && \
sed -i 's/^#alias l/alias l/g' /home/obs/.bashrc
# (crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/arua_close-wait.sh") | crontab -

# driver access url, not needed
# (crontab -l 2>/dev/null; echo "* * * * * /usr/bin/curl http://aagsolo.local/cgi-bin/cgiLastData -o /tmp/aagsolo.txt") | crontab -


# every execution

cp -f *.service /etc/systemd/system/
cp -f arua*.sh /usr/local/bin/
[ ! -d /usr/share/indi/scripts ] && mkdir -p /usr/share/indi/scripts
cp -f *.py /usr/share/indi/scripts/
[ ! -d /home/obs/.indi ] && mkdir -p /home/obs/.indi && chown obs:obs /home/obs/.indi
cp -f *.default /home/obs/.indi/
ls -1 /home/obs/.indi/*.default|xargs -n 1 -I{a} echo {a}|sed 's/.default//'|xargs -r -n 1 -I{b} cp {b}.default {b}
chown obs:obs /home/obs/.indi/*.default
chown obs:obs /home/obs/.indi/*.xml

systemctl daemon-reload

systemctl enable arua_system-obs_ror.service
systemctl restart arua_system-obs_ror.service

systemctl enable arua_system-obs_indiserver.service
systemctl restart arua_system-obs_indiserver.service
