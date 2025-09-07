# https://leetcode.com/problems/lru-cache/

from typing import Any, Generic, TypeVar, Dict, Optional, Callable
from functools import wraps

KEY_T = TypeVar("KEY_T")
VAL_T = TypeVar("VAL_T")

# TODO: add dependency onto normal LL

class Node(Generic[KEY_T, VAL_T]):
    def __init__(
        self,
        key: Optional[KEY_T] = None,
        val: Optional[VAL_T] = None,
        nextN: Optional["Node[KEY_T, VAL_T]"] = None,
        prev: Optional["Node[KEY_T, VAL_T]"] = None,
    ):
        """Initialize a node with key, value, next node, and previous node."""
        self.key: Optional[KEY_T] = key
        self.val: Optional[VAL_T] = val
        self.next: Optional["Node[KEY_T, VAL_T]"] = nextN
        self.prev: Optional["Node[KEY_T, VAL_T]"] = prev

    def __str__(self):
        """Return a string representation of the node."""
        return "[key: {}, val:{}]".format(self.key, self.val)


# TODO: add doublyLinkedList as a standalone class
class DoublyLinkedList(Generic[KEY_T, VAL_T]):
    def __init__(self, capacity: int):
        """Initialize a doubly linked list with a given capacity."""
        self.dummyHead = Node[KEY_T, VAL_T]()
        self.dummyTail = Node[KEY_T, VAL_T](prev=self.dummyHead)
        # assert self.dummyHead.next is None
        self.dummyHead.next = self.dummyTail
        # assert self.dummyTail.prev is None
        self.dummyTail.prev = self.dummyHead
        self.capacity = capacity
        self.len = 0

    def add_head(self, node: Node[KEY_T, VAL_T]) -> Optional[KEY_T]: # Return type can be Optional
        """Add a node to the head of the list. If the list is at capacity, remove the tail and return its key."""
        if self.len == self.capacity:
            assert self.dummyTail.prev is not None 
            temp_key: Optional[KEY_T] = self.dummyTail.prev.key
            tail_node: Node[KEY_T, VAL_T] = self.dummyTail.prev
            self.remove_node(tail_node)
            self.add_node(node)
            return temp_key

        self.add_node(node)
        return None

    def remove_node(self, node: Node[KEY_T, VAL_T]) -> None:
        """Remove a node from the list."""
        assert node.prev is not None
        assert node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev
        self.len -= 1

    def add_node(self, node: Node[KEY_T, VAL_T]) -> None:
        """Add a node to the head of the list."""
        # adding to head
        assert self.dummyHead.next is not None # Assert not None before accessing
        node.next = self.dummyHead.next
        node.prev = self.dummyHead
        node.next.prev = node
        self.dummyHead.next = node
        self.len += 1

    def __str__(self):
        """Return a string representation of the list."""
        temp: Optional[Node[KEY_T, VAL_T]] = self.dummyHead # temp can be Optional
        toPrint = ""
        while temp:
            toPrint += str(temp) + "\n"
            temp = temp.next
        return toPrint

    def get_head(self) -> Optional[KEY_T]: # Return type can be Optional
        """Return the key of the head node."""
        if self.len == 0:
            return None
        assert self.dummyHead.next is not None # Assert not None before accessing
        return self.dummyHead.next.key

    def get_tail(self) -> Optional[KEY_T]: # Return type can be Optional
        """Return the key of the tail node."""
        if self.len == 0:
            return None
        assert self.dummyTail.prev is not None # Assert not None before accessing
        return self.dummyTail.prev.key


class LRUCache(Generic[KEY_T, VAL_T]): # Make LRUCache generic
    def __init__(self, capacity: int):
        """Initialize the LRU Cache with a given capacity."""
        self.order = DoublyLinkedList[KEY_T, VAL_T](capacity) # Instantiate with generic types
        # key to node
        self.location: Dict[KEY_T, Node[KEY_T, VAL_T]] = {}

    def get(self, key: KEY_T) -> Optional[VAL_T]: # Return type can be Optional
        """Retrieve the value associated with the key, updating the access order."""
        # print(self.order)
        if key in self.location:
            # change node's accessing order
            node = self.location[key]
            self.order.remove_node(node)
            self.order.add_node(node)
            return node.val
        return None

    def put(self, key: KEY_T, value: VAL_T) -> None:
        """Insert or update the value associated with the key, updating the access order."""
        if key in self.location:
            # change node's accessing order
            node: Node[KEY_T, VAL_T] = self.location[key] # Update node type
            node.val = value
            self.order.remove_node(node)
            self.order.add_node(node)
        else:
            temp: Node[KEY_T, VAL_T] = Node[KEY_T, VAL_T](key, value) # Instantiate with generic types
            self.location[key] = temp
            to_del: Optional[KEY_T] = self.order.add_head(temp) # to_del can be Optional
            if to_del is not None:
                del self.location[to_del]

    def __str__(self) -> str:
        """Return a string representation of the cache."""
        return str(self.order)

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return self.order.len


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
        # The LRUCache here will use the types from the cached function's arguments and return value
        # Since we cannot know these types at the decorator definition time, we use Any for its generics.
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
