import math
from typing import Generic, TypeVar, List

T = TypeVar("T")


class CircularQueue(Generic[T]):
    """A queue is traditionally implemented as a LinkedList.
    Taking inspiration from producer/consumer buffers, a
    queue may also be implemented in a circular fashion similar
    to a buffer, while allowing for dynamic reallocation of memory.
    This is done in a similar fashion to Lists/Vectors, which resizes
    the array based on a fixed constant. By allocating extra memory that
    may not be needed initially, the queue can maintain O(1) push TC.

    As more reallocations are performed, the total size of the array will
    grow exponentially by resize_const ^ # of resize operations.

    This type of queue is particularly advantageous for low latency operations
    by keeping its data in a contiguous portion of memory, which is more
    friendly for the cache versus a LinkedList structure.

    Attributes:
        _capacity (int): The current capacity of the queue.
        _arr (List[T]): The array storing the elements of the queue.
        _pushIdx (int): The index where the next element will be pushed.
        _popIdx (int): The index from which the next element will be popped.
        _size (int): The current size of the queue.
        _resize_const (float): The constant by which the capacity is multiplied when resizing.

    """

    def __init__(self, cap: int, resize_const: float = 1.5):
        """Initializes a CircularQueue with a specified capacity and resize constant.

        Args:
            cap (int): The initial capacity of the queue.
            resize_const (float, optional): The constant by which the capacity is
            multiplied when resizing. Defaults to 1.5.

        """
        self._capacity: int = cap
        self._arr: List[T] = [None] * cap
        self._pushIdx: int = -1
        self._popIdx: int = 0
        self._size: int = 0
        self._resize_const: int = resize_const

    def _resize(self) -> None:
        """Resizes the CircularQueue to a new capacity based on the resize constant.

        This method is called when the queue is full and a new element needs to be added.
        It creates a new array with a capacity that is the product of the current capacity
        and the resize constant, then copies the elements from the old array to the new
        array, maintaining the correct order and indices for push and pop operations.

        """
        new_capacity: int = math.ceil(self._capacity * self._resize_const)
        new_arr: List[T] = [None] * new_capacity
        for i in range(self.size):
            new_arr[i] = self._arr[(i + self._popIdx) % self._capacity]
        self._pushIdx = self._capacity - 1
        self._popIdx = 0
        self._capacity = new_capacity
        self._arr = new_arr

    def push(self, val: T) -> None:
        """Adds a new element to the end of the CircularQueue.

        If the queue is full, it will resize itself before adding the new element.

        Args:
            val: The value to be added to the queue.

        """
        if self.full():
            self._resize()
        self._size += 1
        self._pushIdx = (self._pushIdx + 1) % self._capacity
        self._arr[self._pushIdx] = val

    def pop(self) -> None:
        """Removes and returns the element at the front of the CircularQueue.

        If the queue is empty, it returns None.

        Returns:
            The element at the front of the queue if it's not empty, otherwise None.

        """
        if self.empty():
            return None
        self._size -= 1
        res: T = self._arr[self._popIdx]
        self._popIdx = (self._popIdx + 1) % self._capacity
        return res

    def empty(self) -> bool:
        """Checks if the CircularQueue is empty.

        Returns:
            True if the queue is empty, False otherwise.

        """
        return self._size == 0

    def full(self) -> bool:
        """Checks if the CircularQueue is full.

        Returns:
            True if the queue is full, False otherwise.

        """
        return self._size == self._capacity

    def peek(self) -> None:
        """Returns the element at the front of the CircularQueue without removing it.

        If the queue is empty, it returns None.

        Returns:
            The element at the front of the queue if it's not empty, otherwise None.

        """
        if self.empty():
            return None
        return self._arr[self._popIdx]

    def __len__(self):
        return self._size

    def __str__(self):
        return str(self._arr)
