#!/bin/bash
USB_BUS=$(lsusb|grep Pinnacle|cut -c5-7)
USB_DEVICE=$(lsusb |grep Pinnacle|cut -c16-18)
echo BUS: $USB_BUS DEVICE: $USB_DEVICE
~/usbreset/usbreset /dev/bus/usb/$USB_BUS/$USB_DEVICE
