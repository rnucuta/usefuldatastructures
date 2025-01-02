from collections import defaultdict
# https://leetcode.com/problems/lfu-cache/

class Node:
    def __init__(self, key=0, val=0, next=None, prev=None):
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

    def push(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def pop(self):
        if self.size == 0:
            return None
        node = self.tail.prev
        self.remove(node)
        return node

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.minFreq = 0
        self.cache = {}
        self.freqMap = defaultdict(DoublyLinkedList)
        self.size = 0

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._update(node)
        return node.val

    def put(self, key: int, value: int) -> None:
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

    def _update(self, node):
        freq = node.freq
        self.freqMap[freq].remove(node)
        if freq == self.minFreq and self.freqMap[freq].size == 0:
            self.minFreq += 1

        node.freq += 1
        self.freqMap[node.freq].push(node)