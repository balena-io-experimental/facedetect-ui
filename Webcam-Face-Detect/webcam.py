import cv2
import sys
import os
import threading

pipeFile = "/data/faces"
faces = []
lock = threading.Lock()

def toInt(s):
    return int(s)

def parseFace(face):
    return map(toInt, face.split(','))

def pipeReader():
    while True:
        with open(pipeFile) as openPipe:
            for line in openPipe:
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

video_capture = cv2.VideoCapture('/data/video1')
cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)          
cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    faces = getFacesFromPipe()

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
