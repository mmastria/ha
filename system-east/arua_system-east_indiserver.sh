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

echo "start indi_ieq_telescope -n \"iOptron CEM60\" -c \"~/.indi/iOptron CEM60_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_atik_ccd -n \"Atik 383L+\" -c \"~/.indi/Atik 383L+_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_sx_wheel -n \"SX Wheel\" -c \"~/.indi/SX Wheel_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_qhy_ccd -n \"QHY5LII-M\" -c \"~/.indi/QHY5LII-M_config.xml\"" > ~/.indi/indiFIFO
echo "start \"Armadillo focuser\"@system-main:7625  -n \"Armadillo focuser\" -c \"~/.indi/Armadillo focuser_config.xml\"" > ~/.indi/indiFIFO
echo "start \"Astrometry\"@system-main -n \"Astrometry\" -c \"~/.indi/Astrometry_config.xml\"" > ~/.indi/indiFIFO
echo "start \"AAG Cloud Watcher\"@aagsolo -n \"AAG Cloud Watcher\" -c \"~/.indi/AAG Cloud Watcher_config.xml\"" > ~/.indi/indiFIFO
echo "start \"RollOff Roof\"@system-power -n \"RollOff Roof\" -c \"~/.indi/RollOff Roof_config.xml\"" > ~/.indi/indiFIFO

wait "$child"
echo "stopping indiserver"
exit
