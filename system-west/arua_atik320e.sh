#!/bin/bash

_term() {
  echo "exiting atik320e"
  kill -TERM "$child" >/dev/null 2>&1
  exit
}

echo "starting atik320e"
trap _term SIGTERM SIGINT

echo "start indi_atik_ccd -n \"Atik 320E\"" > ~/.indi/indiFIFO
child=$(ps -ef|grep indi_atik_ccd|grep -v grep|awk '{print $2}'|sort|tail -n 1)

wait "$child"
echo "stopping atik320e"
exit

