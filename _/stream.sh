apt-get install gstreamer-tools
apt-get install ffmpeg
avconv -f video4linux2 -i /dev/video0 -vcodec mpeg2video -r 25 -pix_fmt yuv420p -me_method epzs -b 2600k -bt 256k -f rtp rtp://102.168.0.205:5004
avconv -f video4linux2 -i /dev/video0 -vcodec mpeg2video -r 25 -pix_fmt yuv420p -me_method epzs -b 2600k -bt 256k -f mjpeg - | gst-launch -v fdsrc ! tcpserversink host=192.168.0.205 port=8008


