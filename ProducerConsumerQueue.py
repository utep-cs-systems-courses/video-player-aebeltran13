import threading, cv2, base64, queue

framesQueueLock = threading.Lock()

class producerConsumerQueue():
    def __init__(self):
        self.fullSemaphore = threading.Semaphore(0) #Start with 0 full semaphores
        self.emptySemaphore = threading.Semaphore(16) #Start with 16 empty semaphores
        self.frameQueue = queue.Queue()

    def insert(self, frame):
        self.emptySemaphore.acquire()
        framesQueueLock.acquire()
        self.frameQueue.put(frame)
        framesQueueLock.release()
        self.fullSemaphore.release()

    def remove(self):
        self.fullSemaphore.acquire()
        framesQueueLock.acquire()
        frame = self.frameQueue.get()
        framesQueueLock.release()
        self.emptySemaphore.release()
        return frame

    def empty(self):
        framesQueueLock.acquire()
        isEmpty = self.frameQueue.empty()
        framesQueueLock.release()
        return isEmpty
