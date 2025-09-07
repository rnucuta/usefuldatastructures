# https://leetcode.com/problems/lfu-cache/description/

from collections import defaultdict
from functools import wraps
from typing import Optional, Callable, Any, Hashable, Dict


class Node:
    def __init__(self, 
        key: Hashable = 0, 
        val: Any = 0, 
        next: Optional["Node"] = None, 
        prev: Optional["Node"] = None
    ):
        self.key = key
        self.val = val
        self.freq = 1
        self.next = next
        self.prev = prev


class DoublyLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def push(self, node: "Node") -> None:
        """Inserts a new node at the beginning of the doubly linked list.

        This method adds a new node to the front of the list, updating the next and previous pointers of adjacent nodes accordingly.

        Args:
            node (Node): The node to be inserted into the list.

        """
        node.next = self.head.next
        node.prev = self.head
        assert self.head.next is not None
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def pop(self) -> Optional["Node"]:
        """Removes and returns the last node from the doubly linked list.

        This method removes the last node from the list and returns it. If the list is empty, it returns None.

        Returns:
            Node: The last node from the list, or None if the list is empty.

        """
        if self.size == 0:
            return None
        node = self.tail.prev
        assert node is not None
        self.remove(node)
        return node

    def remove(self, node: "Node") -> None:
        """Removes a node from the doubly linked list.

        This method removes the specified node from the list, updating the next and previous pointers
        of adjacent nodes accordingly.

        Args:
            node (Node): The node to be removed from the list.

        """
        assert node.prev is not None
        assert node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1


class LFUCache:
    """A class representing a Least Frequently Used (LFU) Cache.
    Now supports any hashable key and any value type.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.minFreq = 0
        self.cache: Dict[Hashable, Node] = {}
        self.freqMap = defaultdict(DoublyLinkedList)
        self.size = 0

    def get(self, key: Hashable) -> Any:
        """Retrieves the value associated with the given key from the cache.

        This method retrieves the value associated with the given key from the cache.
        If the key is not present in the cache, it returns -1.

        Args:
            key (int): The key to retrieve the value for.

        Returns:
            int: The value associated with the key if present, otherwise -1.

        """
        if key not in self.cache:
            raise KeyError(key)
        node = self.cache[key]
        self._update(node)
        return node.val

    def put(self, key: Hashable, value: Any) -> None:
        """Inserts or updates a key-value pair in the cache.

        This method inserts a new key-value pair into the cache or updates the value of an existing key.
        If the cache is full and a new key-value pair is inserted, the least frequently used item is evicted
        to make space for the new pair.

        Args:
            key (int): The key of the pair to be inserted or updated.
            value (int): The value associated with the key.

        """
        if self.capacity == 0:
            return

        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._update(node)
        else:
            if self.size == self.capacity:
                lfuList = self.freqMap[self.minFreq]
                evicted = lfuList.pop()
                assert evicted is not None
                del self.cache[evicted.key]
                self.size -= 1

            node = Node(key, value)
            self.cache[key] = node
            self.freqMap[1].push(node)
            self.minFreq = 1
            self.size += 1

    def _update(self, node: "Node") -> None:
        freq = node.freq
        self.freqMap[freq].remove(node)
        if freq == self.minFreq and self.freqMap[freq].size == 0:
            self.minFreq += 1

        node.freq += 1
        self.freqMap[node.freq].push(node)


def lfu_cache(maxsize: int = 128) -> Callable[..., Any]:
    """A function decorator that implements a Least Frequently Used (LFU) cache.

    This decorator caches the results of a function call. If the function is called
    again with the same arguments, the cached result is returned instead of
    re-executing the function. When the cache reaches its `maxsize`, the least
    frequently used item is discarded to make room for new items.

    Args:
        maxsize (int, optional): The maximum number of items to store in the cache.
                                 Defaults to 128.

    Returns:
        Callable: A decorator function that can be applied to another function
                  to enable LFU caching.

    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache = LFUCache(maxsize)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create a key from args and sorted kwargs
            # to prevent duplicate calls (must be hashable)
            key = (args, tuple(sorted(kwargs.items())))
            try:
                return cache.get(key)
            except KeyError:
                result = func(*args, **kwargs)
                cache.put(key, result)
                return result

        return wrapper

    return decorator
