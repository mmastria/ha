#!/bin/bash

_term() {
  echo "exiting indiserver"
  kill -TERM "$child" >/dev/null 2>&1
  exit
}

echo "starting indiserver"
trap _term SIGTERM SIGINT

[ -d ~/.indi ] || mkdir ~/.indi
ps -ef|grep /usr/bin/indiserver|grep -v grep|{ read a b n;echo $b; }|xargs -r -n 1 kill -TERM
[ -p ~/.indi/indiFIFO ] && rm -f ~/.indi/indiFIFO
mkfifo ~/.indi/indiFIFO
/usr/bin/indiserver -p 7624 -m 100 -v -f ~/.indi/indiFIFO &
child=$!

echo "start indi_wiringpi_gpio -n \"Power System\" -c \"$HOME/.indi/Power System_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_script_dome -n \"Dome Scripting Gateway\" -c \"$HOME/.indi/Dome Scripting Gateway_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_watchdog -n \"WatchDog\" -c \"$HOME/.indi/WatchDog_config.xml\"" > ~/.indi/indiFIFO
echo "start \"Weather Meta\"@system-env:7624" > ~/.indi/indiFIFO

/usr/share/indi/scripts/loadDriver "Power System"
/usr/share/indi/scripts/loadDriver "Dome Scripting Gateway"
/usr/share/indi/scripts/loadDriver "Weather Meta"

wait "$child"
echo "stopping indiserver"
exit
