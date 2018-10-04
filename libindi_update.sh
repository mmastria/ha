#!/bin/bash
pushd ~
[ -d libindi.old ] && rm -rf libindi.old
[ -f libindi_rpi.tar.gz ] && mkdir libindi.old && mv libindi_* libindi.old/
curl http://indilib.org/download/raspberry-pi/send/6-raspberry-pi/9-indi-library-for-raspberry-pi.html -o libindi_rpi.tar.gz
tar -zxvf libindi_rpi.tar.gz
echo ""
echo "*** VERIFICANDO ATUALIZACOES ***"
echo ""
[ -d libindi.old ] && diff libindi_1*/ libindi.old/libindi_1*/
[ -d libindi.old ] && [ $(diff libindi_1*/ libindi.old/libindi_1*/ | wc -l) -eq 0 ] && popd && echo "*** SEM NOVAS ATUALIZACOES ***" &&  exit
echo ""
echo "*** ATUALIZANDO ***"
echo ""
cd libindi_1*
ls -1 /etc/systemd/system/multi-user.target.wants/|grep arua|cut -d / -f 6|xargs -n 1 -r -t systemctl stop
dpkg -i *.deb
apt -y --fix-broken install
dpkg -i *.deb
ls -1 /etc/systemd/system/multi-user.target.wants/|grep arua|cut -d / -f 6|xargs -n 1 -r -t systemctl start
popd

