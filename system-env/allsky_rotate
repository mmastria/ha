#!/bin/sh
cd /var/www/html
FILE="allsky_$(date -d 'yesterday 13:00' +%Y%m%d)"
FILELIST="${FILE}-*.jpg"
ffmpeg -y -pattern_type glob -i ${FILE}'-*.jpg' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -pix_fmt yuv420p ${FILE}.mp4
tar -zcvf ${FILE}.tgz $FILELIST
rm -f $FILELIST

