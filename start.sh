#!/bin/bash
set -e

# Disable DPMS / Screen blanking
xset -dpms
xset s off
xset s noblank

if [ ! -p /data/faces ]; then
	mkfifo /data/faces
fi

cd ./Webcam-Face-Detect
python2.7 webcam.py
