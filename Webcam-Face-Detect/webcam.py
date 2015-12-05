import cv2
import sys
import os
import threading
import time
import json
import urllib2

appToQuery = os.environ.get('ALGORITHM_APP_ID')
if not appToQuery:
    appToQuery = '9089'

pipeFile = "/data/faces"
faces = []
facesLock = threading.Lock()
statusLock = threading.Lock()
deviceStatus = ''

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
            facesLock.acquire()
            faces = f
            facesLock.release()

def deviceStatusReader():
    global deviceStatus
    while True:
        status = {}
        try:
            status = json.load(urllib2.urlopen(os.environ.get('RESIN_SUPERVISOR_ADDRESS') + '/v1/device?appId=' + appToQuery + '&apikey=' + os.environ['RESIN_SUPERVISOR_API_KEY']))
        except urllib2.HTTPError:
            print('Failed to get device status')
        statusLock.acquire()
        if 'download_progress' in status:
            deviceStatus = 'Downloading new algorithm: ' + str(status['download_progress']) + '%'
        elif 'commit' in status:
            deviceStatus = 'Algorithm version ' + status['commit']
        else:
            deviceStatus = 'Unkown algorithm version'
        statusLock.release()
        time.sleep(1)

def getFacesFromPipe():
    facesLock.acquire()
    f = faces
    facesLock.release()
    return f

def getDeviceStatus():
    statusLock.acquire()
    status = deviceStatus
    statusLock.release()
    return status

t = threading.Thread(target=pipeReader)
t.start()

t2 = threading.Thread(target=deviceStatusReader)
t2.start()

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
        status = getDeviceStatus()

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
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, status, (10, 710), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 2)
            cv2.imshow("Video", frame)

        cv2.waitKey(1)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
