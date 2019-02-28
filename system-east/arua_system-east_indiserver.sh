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

echo "start indi_ieq_telescope -n \"iOptron CEM60\" -c \"$HOME/.indi/iOptron CEM60_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_atik_ccd -n \"Atik 383L+\" -c \"$HOME/.indi/Atik 383L+_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_sx_wheel -n \"SX Wheel\" -c \"$HOME/.indi/SX Wheel_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_qhy_ccd -n \"QHY5LII-M\" -c \"$HOME/.indi/QHY5LII-M_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_astrometry -n \"Astrometry\" -c \"$HOME/.indi/Astrometry_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_watchdog -n \"WatchDog\" -c \"$HOME/.indi/WatchDog_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_armadillo_focus -n \"Armadillo focuser\" -c \"$HOME/.indi/Armadillo focuser_config.xml\"" > ~/.indi/indiFIFO
#echo "start \"Armadillo focuser Main\"@system-obs:7624" > ~/.indi/indiFIFO
echo "start \"Weather Meta\"@system-obs:7624" > ~/.indi/indiFIFO
echo "start \"Dome Scripting Gateway\"@system-obs:7624" > ~/.indi/indiFIFO
#echo "start \"Observ Cam\"@system-obs:7624" > ~/.indi/indiFIFO
#echo "start indi_v4l2_ccd -n \"East Camera\" -c \"$HOME/.indi/East Camera_config.xml\"" > ~/.indi/indiFIFO

wait "$child"
echo "stopping indiserver"
exit
