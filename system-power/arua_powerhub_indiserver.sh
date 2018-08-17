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
/usr/bin/indiserver -p 7624 -m 100 -v -f ~/.indi/indiFIFO &
child=$!

echo "start indi_duino -c \"~/.indi/arua_powerhub_config.xml\" -n \"Power HUB\" -s \"/usr/share/indi/arua_powerhub_sk.xml\"" > ~/.indi/indiFIFO

wait "$child"
echo "stopping indiserver"
exit

