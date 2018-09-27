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

#echo "start indi_ioptronv3_telescope -n \"iOptron CEM120\" -c \"$HOME/.indi/iOptron CEM120_config.xml\"" > ~/.indi/indiFIFO
#echo "start indi_atik_ccd -n \"Atik 320E\" -c \"$HOME/.indi/Atik 320E_config.xml\"" > ~/.indi/indiFIFO
#echo "start indi_qhy_ccd -n \"QHY5LII-M\" -c \"$HOME/.indi/QHY5LII-M_config.xml\"" > ~/.indi/indiFIFO
#echo "start \"Armadillo focuser\"@system-main:7626" > ~/.indi/indiFIFO
#echo "start \"Astrometry\"@system-main:7626" > ~/.indi/indiFIFO
#echo "start \"AAG Cloud Watcher\"@system-weather:7624" > ~/.indi/indiFIFO
#echo "start \"Vantage\"@system-weather:7624" > ~/.indi/indiFIFO
#echo "start \"V4L2 CCD\"@system-weather:7624" > ~/.indi/indiFIFO
#echo "start \"RollOff Roof\"@system-power:7625" > ~/.indi/indiFIFO

#echo "start indi_rolloff_dome" > ~/.indi/indiFIFO
echo "start indi_script_dome" > ~/.indi/indiFIFO

wait "$child"
echo "stopping indiserver"
exit
