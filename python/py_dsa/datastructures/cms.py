from typing import List
# TODO: add functionality for all hashable types


class CountMinSketch:
    """A Count-Min Sketch is a probabilistic data structure that is used to
    estimate the frequency of elements in a stream of data. It is particularly
    useful for counting the frequency of items in a stream where the items are
    too numerous to be stored in memory. The Count-Min Sketch is a compact summary
    of the frequency of elements in a stream, allowing for fast and approximate frequency queries.
    """

    def __init__(self, a: List[int], b: List[int], p: List[int], w: int):
        self.a = a  # random vector with positive entries with length d
        self.b = b  # random vector with positive entries with length d
        self.p = p  # prime number
        self.w = w  # width of the sketch matrix
        self.d = len(a)  # number of hash functions/depth of the sketch matrix
        self.count = [[0] * self.w for _ in range(self.d)]  # sketch matrix

    def update(self, item: int) -> None:
        """Update the count of the given item in the Count-Min Sketch.

        Args:
            item (int): The item to update the count for.

        """
        for i in range(self.d):
            self.count[i][self.h_i(i, item)] += 1

    def retrieve(self, item: int) -> int:
        """Retrieve the count of the given item in the Count-Min Sketch.

        Args:
            item (int): The item to retrieve the count for.

        Returns:
            int: The count of the given item in the Count-Min Sketch.

        """
        min_count = float("inf")
        for i in range(self.d):
            min_count = min(min_count, self.count[i][self.h_i(i, item)])
        return min_count

    def h_i(self, i: int, x: int) -> int:
        """Compute the hash value for the given item and hash function index.

        Args:
            i (int): The index of the hash function.
            x (int): The item to hash.

        Returns:
            int: The hash value of the item using the specified hash function.

        """
        return ((self.a[i] * x + self.b[i]) % self.p) % self.w
