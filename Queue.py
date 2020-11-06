import queue
from threading import Lock, Semaphore

class ThreadyQueue:
    def __init__(self, maxcount):
        self.base_q = queue.Queue()
        self.lock = Lock()
        self.queue_spots = Semaphore(maxcount)
        self.not_empty = Semaphore(0)
    
    def put(self, item):
        self.queue_spots.acquire()
        self.lock.acquire()
        self.base_q.put(item)
        self.lock.release()
        self.not_empty.release()

    def get(self):
        self.not_empty.acquire()
        self.lock.acquire()
        item = self.base_q.get()
        self.lock.release()
        self.queue_spots.release()
        
        return item
