from collections import defaultdict
import heapq

class MaxStack:
    def __init__(self):
        self._stack = list()
        self._heap = list()
        self._order_counter = defaultdict(int)
        
    def _clean_stack(self):
        while self._stack and not self._stack[-1][2]:
            self._stack.pop()
        
    def _clean_heap(self):
        while self._heap and not self._heap[0][2]:
            heapq.heappop(self._heap)
            
    def _inc_count(self, key):        
        count = self._order_counter[key]
        self._order_counter[key] += 1
        return count
        
    def _dec_count(self, key):    
        self._order_counter[key] -= 1
        if not self._order_counter[key]:
            del self._order_counter[key]
            
    def push(self, x: int) -> None:
        order_index = self._inc_count(x)
        
        node = [-x, -order_index, True]
        self._stack.append(node)
        heapq.heappush(self._heap, node)
        
    def pop(self) -> int:
        self._clean_stack()
        node = self._stack.pop()
        node[2] = False
        val = -node[0]
        
        self._dec_count(val)
        self._clean_stack()
        return val

    def top(self) -> int:
        return -self._stack[-1][0]
        
    def peekMax(self) -> int:
        self._clean_heap()
        return -self._heap[0][0]
        
    def popMax(self) -> int:
        self._clean_heap()
        node = heapq.heappop(self._heap)
        node[2] = False
        val = -node[0]
        
        self._dec_count(val)
        self._clean_stack()
        return val