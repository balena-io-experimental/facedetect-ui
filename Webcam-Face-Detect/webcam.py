import cv2
import sys
import os
import threading
import time

pipeFile = "/data/faces"
faces = []
lock = threading.Lock()

def toInt(s):
    return int(s)

def parseFace(face):
    return map(toInt, face.split(','))

def pipeReader():
    global faces
    while True:
        openPipe = open(pipeFile, 'r')
        for line in openPipe:
            print(line)
            f = map(parseFace, line.split(';'))
            lock.acquire()
            faces = f
            lock.release()

def getFacesFromPipe():
    lock.acquire()
    f = faces
    lock.release()
    return f

t = threading.Thread(target=pipeReader)
t.start()

cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video", 1280, 720)

while True:
    video_capture = cv2.VideoCapture('/usr/src/FaceDetect/video.sdp')
    if not video_capture:
        time.sleep(0.1)
        continue
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            video_capture.release()
            time.sleep(0.1)
            break

        ff = getFacesFromPipe()

        # Display the resulting frame
        if len(frame) > 0:
            # Draw a rectangle around the faces
            if len(ff) > 0:
                for t in ff:
                    if len(t) == 4:
                        x = t[0]
                        y = t[1]
                        w = t[2]
                        h = t[3]                    
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Video", frame)

        cv2.waitKey(1)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
