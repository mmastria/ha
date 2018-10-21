/usr/share/indi/scripts/indi_watcher_weather_close.py
lsof -i :80 |grep CLOSE_WAIT| awk '{print $2}'|uniq|xargs -r kill
/usr/share/indi/scripts/indi_watcher_weather.py
