#!/bin/sh
pushd /var/www/html/
ffmpeg -y -pattern_type glob -i 'allsky_*.jpg' -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -pix_fmt yuv420p parcial.mp4
popd
