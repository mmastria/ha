#!/bin/bash

_term() {
  echo "exiting indiserver"
  kill -TERM "$child" >/dev/null 2>&1
  exit
}

echo "starting indiserver"
trap _term SIGTERM SIGINT

[ -p ~/.indi/indiFIFO ] && rm -f ~/.indi/indiFIFO
mkfifo ~/.indi/indiFIFO
/usr/bin/indiserver -p 7624 -m 100 -v \
  "Astrometry"@system-main \
  "Armadillo focuser"@system-main:7625 \
  "AAG Cloud Watcher"@aagsolo \
  "RollOff Roof"@system-power \
  -f ~/.indi/indiFIFO &
child=$!

#echo "start \"Astrometry\"@system-main -n \"Astrometry\"" > ~/.indi/indiFIFO

wait "$child"
echo "stopping indiserver"
exit
