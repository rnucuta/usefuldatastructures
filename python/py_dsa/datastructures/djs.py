from typing import List, TypeVar, Generic
from collections.abc import Hashable

T = TypeVar("T", bound=Hashable)


class DisjointSet(Generic[T]):
    """A Disjoint Set is a data structure that keeps track of a set of elements
    partitioned into a number of disjoint (non-overlapping) subsets. It provides
    operations for adding new sets, merging existing sets, and finding the
    representative of a set. The time complexity of these search is O(α(n)) due to
    path compression as performed in the link algorithm, where n is the number of
    elements in the disjoint set, and inserting an element is O(1) time. In practice,
    search has a nearly constant time complexity as the inverse ackman function grows
    quite slowly as n increases. For n <= 2^(2^16), α(n) <= 5.
    """

    def __init__(self, start_size: int, start_keys: List["T"]):
        assert start_size >= 0
        assert len(start_keys) == start_size

        self.parent = [0] * (start_size + 1)
        self.idx_key_map = [None] + [k for k in start_keys]
        self.key_idx_map = {k: i + 1 for i, k in enumerate(start_keys)}
        self._num_djsets = start_size

    def add_key(self, key: "T") -> None:
        """Adds a new key to the disjoint set.

        This method adds a new key to the disjoint set,
        updating the internal data structures accordingly.

        Args:
            key (T): The key to be added to the disjoint set.

        """
        assert key not in self.key_idx_map, (
            "KeyExists: Key already exists in the index map"
        )

        self.key_idx_map[key] = len(self.parent)
        self.parent.append(0)
        self.idx_key_map.append(key)
        self._num_djsets += 1

    def find_set(self, u: "T") -> "T":
        """Finds the set of the given element.

        This method finds the set of the given element by recursively following
        the parent pointers until it finds the root of the set.

        Args:
            u (T): The element to find the set for.

        Returns:
            T: The root of the set containing the given element.

        """
        u_parent_idx = self._find_set(self.key_idx_map[u])
        return self.idx_key_map[u_parent_idx]

    def _find_set(self, u: int) -> int:
        """Finds the set of an element recursively using path compression.

        This method finds the set of an element by recursively following
        the parent pointers until it finds the root of the set. It also
        applies path compression to optimize the tree structure.

        Args:
            u (int): The index of the element to find the set for.

        Returns:
            int: The index of the root of the set containing element u.

        """
        if self.parent[u] <= 0:
            return u
        self.parent[u] = self._find_set(self.parent[u])
        return self.parent[u]

    def link(self, u: "T", v: "T") -> None:
        """Links two disjoint sets containing elements u and v.

        This method merges the disjoint sets containing elements u and v.
        It assumes that u and v are the roots of their respective disjoint sets.

        Args:
            u (T): The first element.
            v (T): The second element.

        """
        idx_u = self.key_idx_map[u]
        idx_v = self.key_idx_map[v]

        assert self.parent[idx_u] <= 0 and self.parent[idx_v] <= 0, (
            "Can only link parents of djsets, use find_set first to get parent"
        )

        if self.parent[idx_u] < self.parent[idx_v]:
            self.parent[idx_v] = idx_u
        else:
            if self.parent[idx_u] == self.parent[idx_v]:
                self.parent[idx_v] -= 1
            self.parent[idx_u] = idx_v

        self._num_djsets -= 1

    def union(self, u: "T", v: "T") -> bool:
        """Unites the disjoint sets containing elements u and v.

        This method merges the disjoint sets containing elements u and v.
        If the elements are already in the same set, it does nothing.

        Args:
            u (T): The first element.
            v (T): The second element.

        Returns:
            bool: True if the union was successful, False if the elements
            were already in the same set.

        """
        parent_u, parent_v = self.find_set(u), self.find_set(v)
        if parent_u != parent_v:
            self.link(parent_u, parent_v)
            return True
        return False

    def get_num_djsets(self) -> int:
        """Returns the number of disjoint sets in the data structure.

        Returns:
            int: The number of disjoint sets.

        """
        return self._num_djsets
