# https://leetcode.com/problems/max-stack/description/

from collections import defaultdict
import heapq


class MaxStack:
    """A stack that supports push, pop, top, peekMax, and popMax operations.
    It keeps track of the maximum element in the stack efficiently.
    """

    def __init__(self):
        self._stack = list()
        self._heap = list()
        self._order_counter = defaultdict(int)

    def _clean_stack(self) -> None:
        """Cleans up the stack by removing elements that have been marked as popped."""
        while self._stack and not self._stack[-1][2]:
            self._stack.pop()

    def _clean_heap(self) -> None:
        """Cleans up the heap by removing elements that have been marked as popped."""
        while self._heap and not self._heap[0][2]:
            heapq.heappop(self._heap)

    def _inc_count(self, key: int) -> int:
        """Increments the count of the given key in the order counter.

        Args:
            key (int): The key to increment.

        Returns:
            int: The previous count of the key.

        """
        count = self._order_counter[key]
        self._order_counter[key] += 1
        return count

    def _dec_count(self, key: int) -> None:
        """Decrements the count of the given key in the order counter.

        Args:
            key (int): The key to decrement.

        """
        self._order_counter[key] -= 1
        if not self._order_counter[key]:
            del self._order_counter[key]

    def push(self, x: int) -> None:
        """Pushes an integer onto the stack.

        Args:
            x (int): The integer to push onto the stack.

        """
        order_index = self._inc_count(x)

        node = [-x, -order_index, True]
        self._stack.append(node)
        heapq.heappush(self._heap, node)

    def pop(self) -> int:
        """Removes and returns the top element of the stack.

        Returns:
            int: The top element of the stack.

        """
        self._clean_stack()
        node = self._stack.pop()
        node[2] = False
        val = -node[0]

        self._dec_count(val)
        self._clean_stack()
        return val

    def top(self) -> int:
        """Gets the top element of the stack without removing it.

        Returns:
            int: The top element of the stack.

        """
        return -self._stack[-1][0]

    def peekMax(self) -> int:
        """Retrieves the maximum element in the stack without removing it.

        Returns:
            int: The maximum element in the stack.

        """
        self._clean_heap()
        return -self._heap[0][0]

    def popMax(self) -> int:
        """Removes and returns the maximum element in the stack.

        Returns:
            int: The maximum element in the stack.

        """
        self._clean_heap()
        node = heapq.heappop(self._heap)
        node[2] = False
        val = -node[0]

        self._dec_count(val)
        self._clean_stack()
        return val
