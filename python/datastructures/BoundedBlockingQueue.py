import threading
from collections import deque

class BoundedBlockingQueue(object):
    def __init__(self, capacity: int):
        self.dq = deque([], maxlen = capacity)
        self._capacity = capacity
        self._length = 0
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)
        self.mux = threading.Semaphore(1)

    def enqueue(self, element: int) -> None:
        self.empty.acquire()
        self.mux.acquire()
        self.dq.append(element)
        self._length += 1
        self.mux.release()
        self.full.release()

    def dequeue(self) -> int:
        self.full.acquire()
        self.mux.acquire()
        res = self.dq.popleft()
        self._length -= 1
        self.mux.release()
        self.empty.release()
        return res
        
    def size(self) -> int:
        return self._length