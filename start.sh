#!/bin/bash
set -e

# Disable DPMS / Screen blanking
xset -dpms
xset s off
xset s noblank

if [ ! -p /data/faces ]; then
	mkfifo /data/faces
fi

if [ ! -p /data/video1 ]; then
	mkfifo /data/video1
fi

if [ ! -p /data/video2 ]; then
	mkfifo /data/video2
fi

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf

supervisorctl -c /etc/supervisor/supervisord.conf start ffserver

while [ ! -f /var/log/ffserver.log ]; do
	sleep 1
done

tail -fn 100 /var/log/ffserver.log &

supervisorctl -c /etc/supervisor/supervisord.conf start ffmpeg

cd ./Webcam-Face-Detect
python2.7 webcam.py &

while [ ! -f /var/log/ffmpeg.log ]; do
	sleep 1
done

tail -fn 100 /var/log/ffmpeg.log &


while [ ! -f /var/log/ffmpeg_error.log ]; do
	sleep 1
done

tail -fn 100 /var/log/ffmpeg_error.log &

while [ ! -f /var/log/ffserver_error.log ]; do
	sleep 1
done

tail -fn 100 /var/log/ffserver_error.log
