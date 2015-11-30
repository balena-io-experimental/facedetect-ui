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

ffmpeg -f video4linux2 -s 800x600 -i /dev/video0 -f avi -y /data/video1 -f avi -y /data/video2 &

cd ./Webcam-Face-Detect
python2.7 webcam.py
