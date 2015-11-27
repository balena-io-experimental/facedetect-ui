#!/bin/bash
set -e

# Disable DPMS / Screen blanking
xset -dpms
xset s off
xset s noblank


if [ ! -p /data/faces ]; then
	mkfifo /data/faces
fi

mount -t devtmpfs /dev
modprobe vv4l2loopback devices=2
ffmpeg -f video4linux2 -s 800x600 -i /dev/video0 -codec copy -f v4l2 /dev/video1 -codec copy -f v4l2 /dev/video2

cd ./Webcam-Face-Detect
python2.7 webcam.py
