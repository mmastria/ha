#!/bin/bash
[ "$(mount|grep /dev/root.*\(ro,|wc -l)" == "1" ] && mount -o remount,rw /dev/root /
[ "$(mount|grep /dev/boot.*\(ro,|wc -l)" == "1" ] && mount -o remount,rw /dev/boot /boot
apt update
apt -y upgrade
apt -y dist-upgrade
[ "$(uname -a|grep aagsolo|wc -l)" == "0" ] && rpi-update

