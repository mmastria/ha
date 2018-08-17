#!/bin/bash

_term() {
  echo "exiting cem120"
  kill -TERM "$child" >/dev/null 2>&1
  exit
}

echo "starting cem120"
trap _term SIGTERM SIGINT

echo "start indi_ioptronv3_telescope -n \"iOptron CEM120\" -c \"~/.indi/indi_ioptronv3_telescope_config.xml\"" > ~/.indi/indiFIFO
child=$(ps -ef|grep indi_ioptronv3_telescope|grep -v grep|awk '{print $2}'|sort|tail -n 1)

wait "$child"
echo "stopping cem120"
exit

