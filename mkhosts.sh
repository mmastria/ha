#!/bin/bash

_mkhosts() {
  ping -q -c 1 $1.local > /dev/null
  if [ $? -eq 0 ]; then
    if [ "$(grep $1 /etc/hosts|grep -v 127|head -n 1)" = "" ]; then
      cp /etc/hosts /tmp/hosts
    else
      grep -v "$(grep $1 /etc/hosts|grep -v 127|head -n 1)" /etc/hosts > /tmp/hosts
    fi
    [[ $(ping -c 1 $1.local|head -n 1) =~ ([0-9]{1,3}.)+([0-9]{1,3}) ]]
    [ "${BASH_REMATCH[0]}" ==  "127.0.0.1" ] || echo -e ${BASH_REMATCH[0]}\\t$1.local $1 >> /tmp/hosts
    mv /tmp/hosts /etc/hosts
  fi
}

_mkhosts system-power
_mkhosts system-east
_mkhosts system-west
_mkhosts system-main
_mkhosts aagsolo

