#!/bin/bash

_term() {
  echo "exiting indiserver"
  kill -TERM "$child" >/dev/null 2>&1
  exit
}

echo "starting indiserver"
trap _term SIGTERM SIGINT

[ -d ~/.indi ] || mkdir ~/.indi
ps -ef|grep /usr/bin/indiserver|grep -v grep|{ read a b c n;echo $c; }|xargs -r -n 1 kill -TERM
[ -p ~/.indi/indiFIFO ] && rm -f ~/.indi/indiFIFO
mkfifo ~/.indi/indiFIFO
/usr/bin/indiserver -p 7624 -m 100 -v -f ~/.indi/indiFIFO &
child=$!

# echo "start indi_astrometry -n \"Astrometry\" -c \"$HOME/.indi/Astrometry_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_wiringpi_gpio -n \"Power System\" -c \"$HOME/.indi/Power System_config.xml\"" > ~/.indi/indiFIFO
/usr/share/indi/scripts/indi_wiringpi_gpio.py
echo "start indi_watcher_weather -n \"AAG Solo Weather\" -c \"$HOME/.indi/AAG Solo Weather_config.xml\"" > ~/.indi/indiFIFO
/usr/share/indi/scripts/indi_watcher_weather.py
echo "start indi_vantage_weather -n \"Vantage\" -c \"$HOME/.indi/Vantage_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_meta_weather -n \"Weather Meta\" -c \"$HOME/.indi/Weather Meta_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_script_dome -n \"Dome Scripting Gateway\" -c \"$HOME/.indi/Dome Scripting Gateway_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_watchdog -n \"WatchDog\" -c \"$HOME/.indi/WatchDog_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_v4l2_ccd -n \"Back Camera\" -c \"$HOME/.indi/Back Camera_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_armadillo_focus -n \"Armadillo focuser Main\" -c \"$HOME/.indi/Armadillo focuser main_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_armadillo_focus -n \"Armadillo focuser Exp\" -c \"$HOME/.indi/Armadillo focuser exp_config.xml\"" > ~/.indi/indiFIFO

wait "$child"
echo "stopping indiserver"
exit
