import cv2, os, time
import threading
import queue
import base64
from ProducerConsumerQueue import producerConsumerQueue

def extractFrames(filename,colorFramesQueue,maxFrames):
    count = 0
    vidcap = cv2.VideoCapture(filename)
    success,image = vidcap.read()

    while success and count < maxFrames:
        success,jpgImage = cv2.imencode('.jpeg',image)
        colorFramesQueue.insert(image)
        success,image = vidcap.read()
        count +=1

def convertToGrayScale(colorFramesQueue,grayScaleFramesQueue):
    while True:
        if colorFramesQueue.empty():
            continue
        else: 
            frame = colorFramesQueue.remove()
            grayScaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grayScaleFramesQueue.insert(grayScaleFrame)
    
def displayFrames(grayScaleFramesQueue):
    while True:
        frame = grayScaleFramesQueue.remove()
        cv2.imshow('Video',frame)
        if grayScaleFramesQueue.empty():
            continue
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        
    cv2.destroyAllWindows()

#Make queues
colorFramesQueue = producerConsumerQueue()
grayScaleFramesQueue = producerConsumerQueue()
fileName = "clip.mp4"
maxFrames = 500

#Make threads
extractFramesThread = threading.Thread(target = extractFrames, args=(fileName,colorFramesQueue,maxFrames))
convertToGrayScalThread = threading.Thread(target = convertToGrayScale, args=(colorFramesQueue, grayScaleFramesQueue))
displayFramesThread = threading.Thread(target = displayFrames, args = (grayScaleFramesQueue))

#Start threads
extractFramesThread.start()
convertToGrayScalThread.start()
displayFramesThread.start()
