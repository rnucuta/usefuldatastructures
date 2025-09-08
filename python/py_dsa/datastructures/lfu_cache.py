# https://leetcode.com/problems/lfu-cache/description/

from collections import defaultdict
from functools import wraps
from typing import TypeVar, Generic, Optional, Callable, Any, Hashable, Dict
from py_dsa.datastructures.doubly_linked_list import DoublyLinkedList, AbstractNode

KEY_T = TypeVar("KEY_T")
VAL_T = TypeVar("VAL_T")

class Node(Generic[KEY_T, VAL_T], AbstractNode["Node"]):
    def __init__(
        self,
        key: KEY_T,
        val: VAL_T,
        next: Optional["Node[KEY_T, VAL_T]"] = None,
        prev: Optional["Node[KEY_T, VAL_T]"] = None,
    ):
        self.key = key
        self.val = val
        self.freq: int = 1
        self.next = next
        self.prev = prev

    def __str__(self):
        """Return a string representation of the node."""
        return "[key: {}, val: {}, freq: {}]".format(self.key, self.val, self.freq)


class LFUCache(Generic[KEY_T, VAL_T]):
    """A class representing a Least Frequently Used (LFU) Cache.
    Now supports any hashable key and any value type.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.minFreq = 0
        self.cache: Dict[KEY_T, Node] = {}
        self.freqMap: Dict[int, DoublyLinkedList] = defaultdict(lambda: DoublyLinkedList())
        self.size = 0

    def get(self, key: KEY_T) -> Optional[VAL_T]:
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

    def put(self, key: KEY_T, value: Any) -> None:
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
                evicted = lfuList.pop_back()
                if evicted:
                    del self.cache[evicted.key]
                    self.size -= 1

            node = Node(key, value)
            self.cache[key] = node
            self.freqMap[1].push_front(node)
            self.minFreq = 1
            self.size += 1

    def _update(self, node: Node) -> None:
        freq = node.freq
        self.freqMap[freq].remove(node)
        if freq == self.minFreq and len(self.freqMap[freq]) == 0:
            self.minFreq += 1

        node.freq += 1
        self.freqMap[node.freq].push_front(node)

    def __str__(self) -> str:
        """Return a string representation of the cache."""
        result = "LFUCache:\n"
        for freq, dll in self.freqMap.items():
            if len(dll) > 0:
                result += f"Freq {freq}: {dll}\n"
        return result

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return self.size


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
