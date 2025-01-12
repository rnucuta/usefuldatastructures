from collections import defaultdict
# TODO: make accessible as function wrapper


class Node:
    def __init__(
        self, key: int = 0, val: int = 0, next: "Node" = None, prev: "Node" = None
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
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def pop(self) -> "Node":
        """Removes and returns the last node from the doubly linked list.

        This method removes the last node from the list and returns it. If the list is empty, it returns None.

        Returns:
            Node: The last node from the list, or None if the list is empty.

        """
        if self.size == 0:
            return None
        node = self.tail.prev
        self.remove(node)
        return node

    def remove(self, node: "Node") -> None:
        """Removes a node from the doubly linked list.

        This method removes the specified node from the list, updating the next and previous pointers
        of adjacent nodes accordingly.

        Args:
            node (Node): The node to be removed from the list.

        """
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1


class LFUCache:
    """A class representing a Least Frequently Used (LFU) Cache.

    This class implements an LFU Cache, which is a type of cache data structure that has limited space,
    and once there are more items than the space, it will preempt the least frequently used item first.
    It provides methods for getting and putting items into the cache, ensuring that the least frequently
    used items are evicted first when the cache is full.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.minFreq = 0
        self.cache = {}
        self.freqMap = defaultdict(DoublyLinkedList)
        self.size = 0

    def get(self, key: int) -> int:
        """Retrieves the value associated with the given key from the cache.

        This method retrieves the value associated with the given key from the cache.
        If the key is not present in the cache, it returns -1.

        Args:
            key (int): The key to retrieve the value for.

        Returns:
            int: The value associated with the key if present, otherwise -1.

        """
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._update(node)
        return node.val

    def put(self, key: int, value: int) -> None:
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
