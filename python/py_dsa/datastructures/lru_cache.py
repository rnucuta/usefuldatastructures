# https://leetcode.com/problems/lru-cache/

from typing import Any, Generic, TypeVar, Dict, Optional, Callable, assert_type
from functools import wraps
from py_dsa.datastructures.doubly_linked_list import DoublyLinkedList, AbstractNode

KEY_T = TypeVar("KEY_T")
VAL_T = TypeVar("VAL_T")

class Node(Generic[KEY_T, VAL_T], AbstractNode["Node"]):
    def __init__(
        self,
        key: Optional[KEY_T] = None,
        val: Optional[VAL_T] = None,
        next: Optional["Node[KEY_T, VAL_T]"] = None,
        prev: Optional["Node[KEY_T, VAL_T]"] = None,
    ):
        """Initialize a node with key, value, next node, and previous node."""
        super().__init__(next, prev)
        self.key = key
        self.val = val

    def __str__(self):
        """Return a string representation of the node."""
        return "[key: {}, val:{}]".format(self.key, self.val)


class LRUCache(Generic[KEY_T, VAL_T]):
    def __init__(self, capacity: int):
        """Initialize the LRU Cache with a given capacity."""
        self.capacity = capacity
        self.order = DoublyLinkedList[Node[KEY_T, VAL_T]]()
        # key to node
        self.location: Dict[KEY_T, Node[KEY_T, VAL_T]] = {}

    def get(self, key: KEY_T) -> Optional[VAL_T]:
        """Retrieve the value associated with the key, updating the access order."""
        if key in self.location:
            # change node's accessing order
            node = self.location[key]
            self.order.move_to_front(node)
            return node.val
        return None

    def put(self, key: KEY_T, value: VAL_T) -> None:
        """Insert or update the value associated with the key, updating the access order."""
        if key in self.location:
            # change node's accessing order
            node: Node[KEY_T, VAL_T] = self.location[key]
            node.val = value
            self.order.move_to_front(node)
        else:
            temp: Node[KEY_T, VAL_T] = Node(key, value)
            self.location[key] = temp
            
            if len(self.order) >= self.capacity:
                # Remove least recently used (tail)
                lru_node = self.order.pop_back()
                if lru_node and lru_node.key is not None:
                    del self.location[lru_node.key] 
            
            self.order.push_front(temp)

    def __str__(self) -> str:
        """Return a string representation of the cache."""
        return str(self.order)

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return len(self.order)


def lru_cache(maxsize: int = 128) -> Callable[..., Any]:
    """A function decorator that implements a Least Recently Used (LRU) cache.

    This decorator caches the results of a function call. If the function is called
    again with the same arguments, the cached result is returned instead of
    re-executing the function. When the cache reaches its `maxsize`, the least
    recently used item is discarded to make room for new items.

    Args:
        maxsize (int, optional): The maximum number of items to store in the cache.
                                 Defaults to 128.

    Returns:
        Callable: A decorator function that can be applied to another function
                  to enable LRU caching.

    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache = LRUCache[Any, Any](maxsize)

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
