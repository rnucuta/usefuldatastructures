class CountMinSketch:
    def __init__(self, a, b, p, w):
        self.a = a # random vector with positive entries with length d
        self.b = b # random vector with positive entries with length d
        self.p = p # prime number
        self.w = w # width of the sketch matrix
        self.d = len(a) # number of hash functions/depth of the sketch matrix
        self.count = [[0] * self.w for _ in range(self.d)] # sketch matrix
    
    def update(self, item) -> None:
        for i in range(self.d):
            self.count[i][self.h_i(i, item)] += 1

    def retrieve(self, item) -> int:
        min_count = float('inf')
        for i in range(self.d):
            min_count = min(min_count, self.count[i][self.h_i(i, item)])
        return min_count

    def h_i(self, i, x) -> int:
        return ((self.a[i] * x + self.b[i]) % self.p) % self.w