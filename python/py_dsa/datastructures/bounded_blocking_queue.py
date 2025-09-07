# https://leetcode.com/problems/design-bounded-blocking-queue/

import threading
from collections import deque
from typing import TypeVar, Generic

T = TypeVar("valT")

class BoundedBlockingQueue(Generic[T]):
    def __init__(self, capacity: "T"):
        self.dq = deque([], maxlen=capacity)
        self._capacity = capacity
        self._length = 0
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)
        self.mux = threading.Semaphore(1)

    def enqueue(self, element: "T") -> None:
        """Adds an element to the end of the queue if the queue is not full.

        Args:
            element (int): The element to be added to the queue.

        Raises:
            ValueError: If the queue is full and cannot accept more elements.

        """
        self.empty.acquire()
        self.mux.acquire()
        self.dq.append(element)
        self._length += 1
        self.mux.release()
        self.full.release()

    def dequeue(self) -> "T":
        """Removes and returns the element at the front of the queue if the queue is not empty.

        Returns:
            T: The element at the front of the queue.

        Raises:
            ValueError: If the queue is empty and cannot dequeue any elements.

        """
        self.full.acquire()
        self.mux.acquire()
        res = self.dq.popleft()
        self._length -= 1
        self.mux.release()
        self.empty.release()
        return res

    def size(self) -> int:
        """Returns the current size of the queue.

        Returns:
            int: The number of elements in the queue.

        """
        return self._length
