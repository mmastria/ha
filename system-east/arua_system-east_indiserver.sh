#!/bin/bash

_term() {
  echo "exiting indiserver"
  kill -TERM "$child" >/dev/null 2>&1
  exit
}

echo "starting indiserver"
trap _term SIGTERM SIGINT

[ -d ~/.indi ] || mkdir ~/.indi
[ -p ~/.indi/indiFIFO ] && rm -f ~/.indi/indiFIFO
mkfifo ~/.indi/indiFIFO
/usr/bin/indiserver -p 7624 -m 100 -v -f ~/.indi/indiFIFO &
child=$!

echo "start indi_ieq_telescope -n \"iOptron CEM60\" -c \"$HOME/.indi/iOptron CEM60_config.xml\"" > ~/.indi/indiFIFO
#echo "start indi_ioptronv3_telescope -n \"iOptron CEM60\" -c \"$HOME/.indi/iOptron CEM60_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_atik_ccd -n \"Atik 383L+\" -c \"$HOME/.indi/Atik 383L+_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_sx_wheel -n \"SX Wheel\" -c \"$HOME/.indi/SX Wheel_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_qhy_ccd -n \"QHY5LII-M\" -c \"$HOME/.indi/QHY5LII-M_config.xml\"" > ~/.indi/indiFIFO
echo "start \"Armadillo focuser\"@system-main:7625" > ~/.indi/indiFIFO
echo "start \"Astrometry\"@system-main:7625" > ~/.indi/indiFIFO
echo "start \"AAG Cloud Watcher\"@aagsolo" > ~/.indi/indiFIFO
echo "start \"RollOff Roof\"@system-power:7625" > ~/.indi/indiFIFO
echo "start \"Vantage\"@aagsolo:7625" > ~/.indi/indiFIFO
echo "start \"V4L2 CCD\"@aagsolo:7626" > ~/.indi/indiFIFO

wait "$child"
echo "stopping indiserver"
exit
