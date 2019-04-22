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

echo "start indi_ioptronv3_telescope -n \"iOptron CEM120\" -c \"$HOME/.indi/iOptron CEM120_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_qhy_ccd -n \"QHY5LII-M\" -c \"$HOME/.indi/QHY5LII-M_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_astrometry -n \"Astrometry\" -c \"$HOME/.indi/Astrometry_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_watchdog -n \"WatchDog\" -c \"$HOME/.indi/WatchDog_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_moonlite_focus" > ~/.indi/indiFIFO
echo "start \"Weather Meta\"@system-env:7624" > ~/.indi/indiFIFO
echo "start \"Dome Scripting Gateway\"@system-obs:7624" > ~/.indi/indiFIFO

/usr/share/indi/scripts/loadDriver.py "Astrometry"
/usr/share/indi/scripts/loadDriver.py "Weather Meta"
/usr/share/indi/scripts/loadDriver.py "Dome Scripting Gateway"

wait "$child"
echo "stopping indiserver"
exit
