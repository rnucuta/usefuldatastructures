import random
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")


class SkipNode:
    """A class representing a node in a Skip List.

    Attributes:
        val (T): The value stored in the node.
        next (List[SkipNode]): A list of references to the next nodes in the Skip List,
        each index representing a level in the Skip List.
        level (int): The level of the node in the Skip List.

    """

    def __init__(self, val: Optional[T], level: int):
        self.val: Optional[T] = val
        self.next: List[Optional[SkipNode]] = [None] * level
        self.level: int = level


class SkipList(Generic[T]):
    """A class representing a Skip List data structure.

    This class implements a Skip List, a probabilistic data structure
    that combines the benefits of a linked list and a binary search tree.
    It allows for efficient insertion, deletion, and search operations
    in O(log(n)) time.

    The ideal value for max_levels is $log_{1/p}(n)$ where n is expected
    number of elements, and p is level-wise probability

    Attributes:
        max_level (int): The maximum level of the Skip List.
        p (float): The probability of a node being promoted to the next level.
        sentinel (SkipNode): The sentinel node at the beginning of the Skip List.
        root (SkipNode): The root node of the Skip List.
        _size (int): The size of the Skip List.

    """

    def __init__(self, max_level: int, p: float):
        self.max_level: int = max_level
        self.p: float = p
        self.sentinel: SkipNode = SkipNode(None, self.max_level)
        self.root: Optional[SkipNode] = None  # root points to the linked list at the bottom level
        self._size = 0

    def insert(self, x: int) -> None:
        """Inserts a new value into the Skip List.

        Args:
            x (int): The value to be inserted into the Skip List.

        """
        # initialize random level
        level = 1
        while random.random() < self.p and level < self.max_level:
            level += 1

        new_node = SkipNode(x, level)

        # find locations to insert at
        # start by iterating through sentinel at top level
        # iterate through respective level until
        # larger value than x is found, or end is hit
        # insert then drop level
        temp = self.sentinel
        for i in range(self.max_level - 1, -1, -1):
            while temp.next[i] and temp.next[i].val < x:
                temp = temp.next[i]
            if i < level:
                new_node.next[i] = temp.next[i]
                temp.next[i] = new_node

        # update root node if inserting at head of list
        if self.root is None or x < self.root.val:
            self.root = new_node

        self._size += 1

    def search(self, x: int) -> Optional[SkipNode]:
        """Searches for a value in the Skip List.

        Args:
            x (int): The value to search for in the Skip List.

        Returns:
            SkipNode: The node containing the value if found, otherwise None.

        """
        temp = self.sentinel
        for i in range(self.max_level - 1, -1, -1):
            while temp.next[i] and temp.next[i].val < x:
                temp = temp.next[i]
            # return as soon as val is found
            if temp.next[i] and temp.next[i].val == x:
                return temp.next[i]

        return None

    def delete(self, x: T) -> None:
        """Deletes a value from the Skip List.

        Args:
            x (T): The value to be deleted from the Skip List.

        """
        if self.root is None:
            return

        # search block
        temp: Optional[SkipNode] = self.sentinel
        for i in range(self.max_level - 1, -1, -1):
            while temp.next[i] and temp.next[i].val < x:
                temp = temp.next[i]
            if temp.next[i] and temp.next[i].val == x:
                temp.next[i] = temp.next[i].next[i]
        if self.root.val == x:
            self.root = self.root.next[0]
            self._size -= 1

    def __len__(self):
        return self._size

    def __str__(self):
        s: List[str] = ["["]
        tmp: Optional[SkipNode] = self.root
        for i in range(self._size):
            if i != self._size - 1:
                s.append(str(tmp.val) + ", ")
                tmp = tmp.next[0]
            else:
                s.append(str(tmp.val) + "]")

        return "".join(s)
