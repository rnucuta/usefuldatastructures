import heapq
from collections import defaultdict


class StreamingMedian:
    """A class to maintain a stream of numbers and efficiently compute the median.
    It uses two heaps: a max-heap for the lower half of numbers and a min-heap for the upper half.
    """

    def __init__(self):
        self.min = []
        self.max = []
        self.min_size = 0
        self.max_size = 0
        self.invalid_nums = defaultdict(int)

    def _cleanMinHeap(self) -> None:
        while self.min and self.invalid_nums[self.min[0]]:
            self.invalid_nums[self.min[0]] -= 1
            heapq.heappop(self.min)

    def _cleanMaxHeap(self) -> None:
        while self.max and self.invalid_nums[-self.max[0]]:
            self.invalid_nums[-self.max[0]] -= 1
            heapq.heappop(self.max)

    def addNum(self, num: int) -> None:
        """Add a number to the data structure.

        Args:
            num (int): The number to be added to the stream.

        """
        self._cleanMinHeap()
        self._cleanMaxHeap()

        heapq.heappush(self.max, -num)
        while self.max and -num != self.max[0] and self.invalid_nums[-self.max[0]]:
            self.invalid_nums[-self.max[0]] -= 1
            heapq.heappop(self.max)
        heapq.heappush(self.min, -heapq.heappop(self.max))
        self.min_size += 1

        if self.min_size > self.max_size:
            self._cleanMinHeap()
            heapq.heappush(self.max, -heapq.heappop(self.min))
            self.min_size -= 1
            self.max_size += 1

    def removeNum(self, num: int) -> None:
        """Remove a number from the data structure.

        Args:
            num (int): The number to be removed from the stream.
                Assumption is this is a valid number to remove.

        """
        self._cleanMinHeap()
        self._cleanMaxHeap()
        self.invalid_nums[num] += 1
        if self.min and num >= self.min[0]:
            self.min_size -= 1
        else:
            self.max_size -= 1

    def getMedian(self) -> float:
        """Retrieve the current median of the stream.

        Returns:
            float: The median of the current stream of numbers.

        """
        self._cleanMinHeap()
        self._cleanMaxHeap()
        if self.max_size == self.min_size:
            return (self.min[0] - self.max[0]) / 2
        else:
            return float(-self.max[0])
