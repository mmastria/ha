#!/bin/bash

_term() {
  echo "exiting qhy5lii"
  kill -TERM "$child" >/dev/null 2>&1
  exit
}

echo "starting qhy5lii"
trap _term SIGTERM SIGINT

echo "start indi_qhy_ccd -n \"QHY5L-II Mono\"" > ~/.indi/indiFIFO
child=$(ps -ef|grep indi_qhy_ccd|grep -v grep|awk '{print $2}'|sort|tail -n 1)

wait "$child"
echo "stopping qhy5lii"
exit

