import queue
from threading import Semaphore

class ThreadyQueue:
    def __init__(self, maxcount):
        self.base_q = queue.Queue()
        self.queue_spots = Semaphore(maxcount)
        self.not_empty = Semaphore(0)
    
    def put(self, item):
        self.queue_spots.acquire()
        self.base_q.put(item)
        self.not_empty.release()

    def get(self):
        self.not_empty.acquire()
        self.queue_spots.release()
        item = self.base_q.get()
        
        return item
