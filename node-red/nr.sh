if [ $# -eq 0 -o ! -d "$1" ];then echo -e "$0 <system-xxxx>";exit 1;fi
SDEVICE="${1///}"
SSED=$(echo "/raspberrypi/ c127.0.0.1\t$SDEVICE \t$SDEVICE.arua")

raspi-config

sed -i 's/en_GB.UTF-8/# en_GB.UTF-8/' /etc/locale.gen
sed -i 's/# en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_TYPE=en_US.UTF-8

locale-gen en_US.UTF-8

dpkg-reconfigure -f noninteractive locales
update-locale en_US.UTF-8

cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
echo "America/Sao_Paulo" > /etc/timezone
dpkg-reconfigure tzdata

git config credential.helper store
git config --global user.email "marco@mastria.com.br"
git config --global user.name "mmastria"
git config --global http.postBuffer 524288000
git pull

passwd <<eof
0
0
eof

sed -i '/^#PermitRootLogin/ c\PermitRootLogin Yes' /etc/ssh/sshd_config
sed -i 's/AcceptEnv LANG/#AcceptEnv LANG/' /etc/ssh/sshd_config
systemctl restart ssh

. ./os_update.sh

sed -i $"$SSED" /etc/hosts
echo $SDEVICE > /etc/hostname
sed -i 's/^# export/export/g' /root/.bashrc
sed -i 's/^# eval/eval/g' /root/.bashrc
sed -i 's/^# alias l/alias l/g' /root/.bashrc

apt-get -y install build-essential git python-dev python-pip vim cmake ntpdate screen 
apt-get -y --fix-broken install
apt-get -y autoremove
apt-get -y clean 
sed -i '/NTPDATE_USE_NTP_CONF/ cNTPDATE_USE_NTP_CONF=no' /etc/default/ntpdate
sed -i '/NTPSERVERS/ cNTPSERVERS="a.st1.ntp.br b.st1.ntp.br c.st1.ntp.br d.st1.ntp.br a.ntp.br b.ntp.br c.ntp.br gps.ntp.br"' /etc/default/ntpdate
timedatectl set-ntp true

[ ! -f /usr/bin/zram.sh ] && \
cp -f zram.sh /usr/bin/ && \
sed -i '$i/usr/bin/zram.sh &' /etc/rc.local

read -p "key to reboot"
reboot



