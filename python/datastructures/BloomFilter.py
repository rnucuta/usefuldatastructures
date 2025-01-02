# TODO: account for optimal sizing

import math
from bitarray import bitarray
import hashlib

class BloomFilter:
    def __init__(self, n, p):
        """
        Initialize the Bloom filter.

        Parameters:
        n (int): Expected number of elements to store.
        p (float): Desired false positive probability.
        """
        # Calculate optimal size of bit array (m) and number of hash functions (k)
        self.m = math.ceil(-n * math.log(p) / (math.log(2) ** 2))
        self.k = math.ceil((self.m / n) * math.log(2))

        # Create a bit array of size m, initialized to 0
        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)

        # Store hash seeds
        self.seeds = range(self.k)

    def _hashes(self, item):
        """
        Generate k hash values for the given item.

        Parameters:
        item (str): The item to hash.

        Returns:
        iter: An iterable of hash values.
        """
        item_str = str(item)
        for seed in self.seeds:
            # Combine the item and seed to generate multiple hash values
            hash_value = int(hashlib.md5((item_str + str(seed)).encode()).hexdigest(), 16)
            yield hash_value % self.m

    def add(self, item):
        """
        Add an item to the Bloom filter.

        Parameters:
        item (str): The item to add.
        """
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

    def contains(self, item):
        """
        Check if an item is in the Bloom filter.

        Parameters:
        item (str): The item to check.

        Returns:
        bool: True if the item might be in the filter, False if it's definitely not.
        """
        return all(self.bit_array[hash_value] for hash_value in self._hashes(item))