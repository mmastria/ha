#!/bin/bash

_term() {
  echo "exiting indiserver"
  kill -TERM "$child" >/dev/null 2>&1
  exit
}

echo "starting indiserver"
trap _term SIGTERM SIGINT

[ -d ~/.indi ] || mkdir ~/.indi
ps -ef|grep /usr/bin/indiserver|grep -v grep|{ read a b n;echo $b; }|xargs -r -n 1 kill -TERM
[ -p ~/.indi/indiFIFO ] && rm -f ~/.indi/indiFIFO
mkfifo ~/.indi/indiFIFO
/usr/bin/indiserver -p 7624 -v -m 100 -f ~/.indi/indiFIFO &
child=$!

echo "start indi_watcher_weather -n \"AAG Solo Weather\" -c \"$HOME/.indi/AAG Solo Weather_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_aagcloudwatcher -n \"AAG Cloud Watcher\" -c \"$HOME/.indi/AAG Cloud Watcher_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_vantage_weather -n \"Vantage\" -c \"$HOME/.indi/Vantage_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_weather_safety_proxy -n \"Weather Safety Proxy\" -c \"$HOME/.indi/Weather Safety Proxy_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_meta_weather -n \"Weather Meta\" -c \"$HOME/.indi/Weather Meta_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_watchdog -n \"WatchDog\" -c \"$HOME/.indi/WatchDog_config.xml\"" > ~/.indi/indiFIFO
echo "start indi_rtlsdr_detector -n \"RTL-SDR Receiver\" -c \"$HOME/.indi/RTL-SDR Receiver_config.xml\"" > ~/.indi/indiFIFO
# http://[ipofcamera]:8080/stream/video/mjpeg
# wget --user=admin --password=YWRtaW4= http://[ipofcamera]:8080/stream/snapshot.jpg
echo "start indi_webcam_ccd -n \"Observ Cam\" -c \"$HOME/.indi/Observ Cam_config.xml\"" > ~/.indi/indiFIFO

/usr/share/indi/scripts/indi_watcher_weather.py &
/usr/share/indi/scripts/indi_aagcloudwatcher.py &
/usr/share/indi/scripts/indi_vantage_weather.py &
/usr/share/indi/scripts/indi_meta_weather.py

wait "$child"
echo "stopping indiserver"
exit
