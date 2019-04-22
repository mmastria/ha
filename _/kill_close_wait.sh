lsof -i :80 |grep CLOSE_WAIT| awk '{print $2}'|uniq|xargs -r kill
