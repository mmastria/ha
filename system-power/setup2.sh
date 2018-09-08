#!/bin/bash

# Arduino Power
# Arduino RolllOffRoof
# RollOffRoof Monitor

[ $(grep powerhub /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash powerhub && \
adduser powerhub dialout && \
adduser powerhub gpio && \
sed -i 's/^#alias l/alias l/g' /home/powerhub/.bashrc

[ $(grep rolloffroof /etc/passwd|wc -l) -eq 0 ] && \
useradd -m -s /bin/bash rolloffroof && \
adduser rolloffroof dialout && \
adduser rolloffroof gpio && \
sed -i 's/^#alias l/alias l/g' /home/rolloffroof/.bashrc

#
# pyindi-client
#
# login as: rolloffroof
# pip2  install --user --install-option="--prefix=/usr/local" pyindi-client

cp -f *.service /etc/systemd/system/
cp -f *.xml /usr/share/indi/
cp -f *.py /usr/local/bin/
cp -f arua*.sh /usr/local/bin/

grep AAG /usr/share/indi/indi_duino.xml > /dev/null 2>&1 || \
cp -f /usr/share/indi/indi_duino.xml /usr/share/indi/indi_duino.xml.ORIGINAL

grep AAG /usr/share/indi/indi_duino.xml > /dev/null 2>&1 || \
sed -i '/<device label="Arduino Servo" skel="servo_sk.xml">/i \
        <device label="Power HUB" skel="arua_powerhub_sk.xml"> \
               <driver name="Power HUB">indi_duino</driver> \
               <version>0.1</version> \
        </device>
' /usr/share/indi/indi_duino.xml

grep AAG /usr/share/indi/indi_duino.xml > /dev/null 2>&1 || \
sed -i '/<devGroup group="Weather">/i \
<devGroup group="Domes"> \
       <device label="RollOff Roof" skel="arua_rolloffroof_sk.xml"> \
               <driver name="RollOff Roof">indi_duino</driver> \
               <version>0.1</version> \
       </device> \
</devGroup> 
' /usr/share/indi/indi_duino.xml

grep AAG /usr/share/indi/indi_duino.xml > /dev/null 2>&1 || \
sed -i '/<device label="Arduino MeteoStation" skel="meteostation_sk.xml">/i \
    <device label="AAG Weather Safe" skel="arua_aagsafe_sk.xml"> \
            <driver name="AAG Weather Safe">indi_duino</driver> \
            <version>0.1</version> \
    </device>
' /usr/share/indi/indi_duino.xml

systemctl daemon-reload

systemctl enable arua_powerhub_indiserver.service
systemctl enable arua_rolloffroof_indiserver.service
systemctl enable arua_rolloffroof_monitor.service

systemctl restart arua_powerhub_indiserver.service
systemctl restart arua_rolloffroof_indiserver.service
systemctl restart arua_rolloffroof_monitor.service


