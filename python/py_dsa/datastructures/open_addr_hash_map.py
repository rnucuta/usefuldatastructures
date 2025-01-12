class HashMap:
    # pythonic implementation of hash map
    # TODO: add more data types (e.g. use id for
    # obj addrs, and java has for str/char
    # public int hashCode() {
    # int hash = 0;
    # for (int i = 0; i < value.length; i++) {
    #     hash = 31 * hash + value[i];
    # }
    # return hash;
    # }
    # inspiration: https://stackoverflow.com/questions/2070276/where-can-i-find-source-or-algorithm-of-pythons-hash-function
    PRIME = 2003
    MAXLF = 2 / 3  # max load factor
    MINLF = 1 / 3  # min laod factor
    MINSIZE = 32

    def __init__(self):
        """Initialize the hash map with a minimum size and zero elements.

        The initial size of the hash map is set to MINSIZE, and the number of
        elements (n) is initialized to zero. An array (arr) is created to
        hold the key-value pairs, initially filled with None.
        """
        self.m = self.MINSIZE
        self.n = 0
        self.arr = [None] * self.m

    def put(self, key: int, value: int) -> None:
        """Insert a key-value pair into the hash map.

        If the load factor (number of elements divided by the size of the array)
        exceeds the maximum load factor (MAXLF), the size of the array is doubled.
        The method computes the hash for the key and finds an appropriate index
        in the array to store the key-value pair. If a collision occurs, it
        uses linear probing to find the next available slot. If the key already
        exists, it updates the value associated with that key.
        """
        if (self.n + 1) / self.m > self.MAXLF:
            self.m *= 2
            new_arr = [None] * self.m
            for v in self.arr:
                if v is not None and v is not False:
                    hashed = (v[0] * self.PRIME) % self.m
                    while new_arr[hashed] is not None:
                        hashed = (hashed + 1) % self.m
                    new_arr[hashed] = v
            self.arr = new_arr

        self.n += 1
        hashed = (key * self.PRIME) % self.m
        while self.arr[hashed] is not None:
            if self.arr[hashed] is not False and self.arr[hashed][0] == key:
                self.arr[hashed][1] = value
                return
            hashed = (hashed + 1) % self.m
        self.arr[hashed] = [key, value]

    def get(self, key: int) -> int:
        """Retrieve the value associated with the given key.

        This method computes the hash for the key and checks the corresponding
        index in the array. If the key is found, it returns the associated value.
        If the key is not found, it returns -1. The method handles collisions
        using linear probing to search for the key.
        """
        hashed = (key * self.PRIME) % self.m
        while self.arr[hashed] is not None:
            if self.arr[hashed] is not False and self.arr[hashed][0] == key:
                return self.arr[hashed][1]
            hashed = (hashed + 1) % self.m
        return -1

    def remove(self, key: int) -> None:
        """Remove the key-value pair associated with the given key.

        This method first checks if the load factor falls below the minimum
        load factor (MINLF). If so, it halves the size of the array. It then
        computes the hash for the key and searches for the key in the array.
        If the key is found, it marks the slot as deleted (by setting it to
        False) and decrements the count of elements (n). If the key is not
        found, no action is taken.
        """
        if self.m > self.MINSIZE and (self.n - 1) / self.m < self.MINLF:
            self.m //= 2
            new_arr = [None] * self.m
            for v in self.arr:
                if v is not None and v is not False:
                    if v[0] == key:
                        self.n -= 1
                        continue
                    hashed = (v[0] * self.PRIME) % self.m
                    while new_arr[hashed] is not None:
                        hashed = (hashed + 1) % self.m
                    new_arr[hashed] = v
            self.arr = new_arr

        else:
            hashed = (key * self.PRIME) % self.m
            while self.arr[hashed] is not None:
                if self.arr[hashed] is not False and self.arr[hashed][0] == key:
                    self.n -= 1
                    self.arr[hashed] = False
                    return
                hashed = (hashed + 1) % self.m
