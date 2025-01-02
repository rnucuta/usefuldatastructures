from heapq import heappush, heappop, heappushpop

# TODO: allow for removal of elements

class MedianFinder:
    def __init__(self):
        self.min = [] # right hand side
        self.max = [] # left hand side
        
    def addNum(self, num: int) -> None:
        heappush(self.min, -heappushpop(self.max, -num))
        if len(self.min) > len(self.max):
            heappush(self.max, -heappop(self.min))
        
    def findMedian(self) -> float:
        if len(self.min) == len(self.max):
            return (self.min[0] + self.max[0] * -1) / 2
        else:
            return -self.max[0]