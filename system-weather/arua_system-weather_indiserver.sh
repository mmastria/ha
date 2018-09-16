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

echo "start indi_aagcloudwatcher -n \"AAG Cloud Watcher\" -c \"$HOME/.indi/AAG Cloud Watcher_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_vantage_weather -n \"Vantage\" -c \"$HOME/.indi/Vantage_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_v4l2_ccd -n \"V4L2 CCD\" -c \"$HOME/.indi/V4L2 CCD_config.xml\"" > ~/.indi/indiFIFO

wait "$child"
echo "stopping indiserver"
exit

