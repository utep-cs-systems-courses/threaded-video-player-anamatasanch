import queue
from threading import Lock, Semaphore

class ThreadyQueue:
    def __init__(self, maxcount):
        self.base_q = queue.Queue()
        self.lock = Lock()
        self.queue_spots = Semaphore(maxcount)
    
    def put(self, item):
        self.queue_spots.acquire()
        self.lock.acquire()
        self.base_q.put(item)
        self.lock.release()

    def get(self):
        self.queue_spots.release()
        self.lock.acquire()
        item = self.base_q.get()
        self.lock.release()
        
        return item
