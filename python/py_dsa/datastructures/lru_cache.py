# https://leetcode.com/problems/lru-cache/

from typing import Generic, TypeVar, Dict
from functools import wraps

KEY_T = TypeVar("KEY_T")
VAL_T = TypeVar("VAL_T")

# TODO: add dependency onto normal LL

class Node:
    def __init__(
        self,
        key: KEY_T = None,
        val: VAL_T = None,
        nextN: "Node" = None,
        prev: "Node" = None,
    ):
        """Initialize a node with key, value, next node, and previous node."""
        self.key = key
        self.val = val
        self.next = nextN
        self.prev = prev

    def __str__(self):
        """Return a string representation of the node."""
        return "[key: {}, val:{}]".format(self.key, self.val)


# doubly linked list stores order of adding to the cache
# most recent at start, oldest at the end
# TODO: add doublyLinkedList as a standalone class
class DoublyLinkedList(Generic[KEY_T, VAL_T]):
    def __init__(self, capacity: int):
        """Initialize a doubly linked list with a given capacity."""
        self.dummyHead = Node()
        self.dummyTail = Node(prev=self.dummyHead)
        self.dummyHead.next = self.dummyTail
        self.capacity = capacity
        self.len = 0

    def add_head(self, node: Node) -> KEY_T:
        """Add a node to the head of the list. If the list is at capacity, remove the tail and return its key."""
        if self.len == self.capacity:
            # pop tail, insert head, return key popped
            temp_key: KEY_T = self.dummyTail.prev.key
            tail_node: Node = self.dummyTail.prev
            self.remove_node(tail_node)
            self.add_node(node)
            return temp_key

        self.add_node(node)
        return None

    def remove_node(self, node: Node) -> None:
        """Remove a node from the list."""
        prev: Node = node.prev
        nextN: Node = node.next
        prev.next = nextN
        nextN.prev = prev
        self.len -= 1

    def add_node(self, node: Node) -> None:
        """Add a node to the head of the list."""
        # adding to head
        node.next = self.dummyHead.next
        node.prev = self.dummyHead
        self.dummyHead.next.prev = node
        self.dummyHead.next = node
        self.len += 1

    def __str__(self):
        """Return a string representation of the list."""
        temp = self.dummyHead
        toPrint = ""
        while temp:
            toPrint += str(temp) + "\n"
            temp = temp.next
        return toPrint

    def get_head(self) -> KEY_T:
        """Return the key of the head node."""
        if self.len == 0:
            return None
        return self.dummyHead.next.key

    def get_tail(self) -> KEY_T:
        """Return the key of the tail node."""
        if self.len == 0:
            return None
        return self.dummyHead.prev.key


class LRUCache:
    def __init__(self, capacity: int):
        """Initialize the LRU Cache with a given capacity."""
        self.order = DoublyLinkedList(capacity)
        # key to node
        self.location: Dict[KEY_T, Node] = {}

    def get(self, key: KEY_T) -> VAL_T:
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
            node: Node = self.location[key]
            node.val = value
            self.order.remove_node(node)
            self.order.add_node(node)
        else:
            temp: Node = Node(key, value)
            self.location[key] = temp
            to_del: KEY_T = self.order.add_head(temp)
            if to_del is not None:
                del self.location[to_del]

    def __str__(self) -> str:
        """Return a string representation of the cache."""
        return str(self.order)

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return self.order.len

def lru_cache(maxsize=128):
    def decorator(func):
        cache = LRUCache(maxsize)

        @wraps(func)
        def wrapper(*args, **kwargs):
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