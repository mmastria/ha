#!/bin/bash
pushd ~
[ -d libindi.old ] && rm -rf libindi.old
[ -f libindi_rpi.tar.gz ] && mkdir libindi.old && mv libindi_* libindi.old/
curl http://indilib.org/download/raspberry-pi/send/6-raspberry-pi/9-indi-library-for-raspberry-pi.html -o libindi_rpi.tar.gz
tar -zxvf libindi_rpi.tar.gz
cd libindi_1*
ls -1 /etc/systemd/system/multi-user.target.wants/arua*|cut -d / -f 6|xargs -n 1 -r -t systemctl stop
dpkg -i *.deb
apt -y --fix-broken install
dpkg -i *.deb
ls -1 /etc/systemd/system/multi-user.target.wants/arua*|cut -d / -f 6|xargs -n 1 -r -t systemctl start
popd
