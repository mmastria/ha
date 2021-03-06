#!/bin/bash

_mkhosts() {
  sed -i "/$1/d" /etc/hosts
  ping -q -c 1 $1.arua > /dev/null
  if [ $? -eq 0 ]; then
    if [ "$(grep $1 /etc/hosts|grep -v 127|head -n 1)" = "" ]; then
      cp /etc/hosts /tmp/hosts
    else
      grep -v "$(grep $1 /etc/hosts|grep -v 127|head -n 1)" /etc/hosts > /tmp/hosts
    fi
    [[ $(ping -c 1 $1.arua|head -n 1) =~ ([0-9]{1,3}.)+([0-9]{1,3}) ]]
    [ "${BASH_REMATCH[0]}" ==  "127.0.0.1" ] || echo -e ${BASH_REMATCH[0]}\\t$1.arua $1 >> /tmp/hosts
    mv /tmp/hosts /etc/hosts
  fi
}

_mkhosts system-east
_mkhosts system-west
_mkhosts system-env
_mkhosts node-red
_mkhosts hassio
_mkhosts aagsolo 
#_mkhosts cem120

