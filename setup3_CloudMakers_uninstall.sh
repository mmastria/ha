#!/bin/bash
pushd ~

cd CloudMakers
ls -1 /etc/systemd/system/multi-user.target.wants/|grep arua|cut -d / -f 6|xargs -n 1 -r -t systemctl stop
ls -1 /etc/systemd/system/multi-user.target.wants/|grep arua|cut -d / -f 6|xargs -n 1 -r -t systemctl disable
rm /usr/bin/indi_atik_ccd
rm /usr/bin/atik_ccd_test
rm /usr/bin/indi_atik_wheel
rm /usr/share/indi/indi_atik.xml
ls -1 *.deb|xargs -n 1 -r dpkg-deb --show|awk '{print $1}'|xargs -r dpkg -P
#apt -y --fix-broken install
popd

