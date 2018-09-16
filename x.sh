#!/bin/bash

if [ $# -eq 0 -o ! -d "$1" ];then echo -e "$0 <system-xxxx>";exit 1;fi
SDEVICE="${1///}"
SSED=$(echo "/raspberrypi/ c127.0.0.1\t$SDEVICE \t$SDEVICE.local")

sed -i $"$SSED" /etc/hosts
echo $SDEVICE > /etc/hostname

