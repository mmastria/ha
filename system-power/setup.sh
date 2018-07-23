[ $(grep powerhub /etc/passwd|wc -l) -eq 0 ] && \
useradd -m powerhub && \
adduser powerhub dialout && \
adduser powerhub gpio

[ $(grep rolloffroof /etc/passwd|wc -l) -eq 0 ] && \
useradd -m rolloffroof && \
adduser rolloffroof dialout && \
adduser rolloffroof gpio

cp -f *.service /etc/systemd/system/
cp -f *_sk.xml /usr/share/indi/
cp -f *.py /usr/local/bin/

systemctl daemon-reload

systemctl enable arua_powerhub_indiserver.service
systemctl enable arua_rolloffroof_indiserver.service
systemctl enable arua_rolloffroof_monitor.service

systemctl restart arua_powerhub_indiserver
systemctl restart arua_rolloffroof_indiserver
systemctl restart arua_rolloffroof_monitor

sleep 1

systemctl status arua_powerhub_indiserver arua_rolloffroof_indiserver arua_rolloffroof_monitor 
