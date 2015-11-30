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

supervisorctl -c /etc/supervisor/supervisord.conf start ffmpeg

cd ./Webcam-Face-Detect
python2.7 webcam.py
