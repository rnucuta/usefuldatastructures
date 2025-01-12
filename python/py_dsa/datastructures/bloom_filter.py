import math
from bitarray import bitarray
import hashlib
from typing import Iterator

# TODO: rewrite with struct lib instead of bitarray


class BloomFilter:
    def __init__(self, n: int, p: float):
        """Initialize the Bloom filter. The optimal size (m) for a bloom filter
        is derived from the desired false positive probability. The number of hash
        functions (k) is derived from the expected size of the bloom filter and the
        expected numbers to be stored, which balances the trade off between the
        number of hash functions and the size of the bit array.

        Args:
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

    def _hashes(self, item: str) -> Iterator[int]:
        """Generate k hash values for the given item.

        Args:
            item (str): The item to hash.

        Returns:
            iter: An iterable of hash values.

        """
        item_str = str(item)
        for seed in self.seeds:
            # Combine the item and seed to generate multiple hash values
            hash_value = int(
                hashlib.md5((item_str + str(seed)).encode()).hexdigest(), 16
            )
            yield hash_value % self.m

    def add(self, item: str) -> None:
        """Add an item to the Bloom filter.

        Args:
        item (str): The item to add.

        """
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

    def contains(self, item: str) -> bool:
        """Check if an item is in the Bloom filter.

        Args:
            item (str): The item to check.

        Returns:
            bool: True if the item might be in the filter, False if it's definitely not.

        """
        return all(self.bit_array[hash_value] for hash_value in self._hashes(item))
