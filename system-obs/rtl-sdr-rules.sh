#!/bin/bash

# Bus 001 Device 006: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T
[ ! -f /lib/udev/rules.d/99-rtl-sdr.rules ] && \
cat > /lib/udev/rules.d/99-rtl-sdr.rules <<- EOF
# RTL2832U OEM vid/pid, e.g. ezcap EzTV668 (E4000), Newsky TV28T (E4000/R820T) etc.
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", MODE:="0666"
EOF
