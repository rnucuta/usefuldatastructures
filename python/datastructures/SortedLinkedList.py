from typing import Generic, TypeVar, List
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class Node:
    """
    A class representing a node in a linked list.

    Attributes:
        val (T): The value stored in the node.
        next (Node): A reference to the next node in the linked list.
    """
    val: T
    next: 'Node' = None


class SortedLinkedList(Generic[T]):
    """
    A class representing a sorted linked list.

    This class implements a sorted linked list, where each node is sorted in 
    ascending order. It provides methods for inserting, searching, and 
    deleting nodes while maintaining the sorted order.

    Attributes:
        root (Node): The root node of the linked list.
        _size (int): The size of the linked list.
    """
    def __init__(self):
        self.root : Node = None
        self._size : int = 0

    def insert(self, x: T) -> None:
        """
        Inserts a new node with the given value into the sorted linked list.

        This method inserts a new node with the value `x` into the sorted linked list, 
        maintaining the sorted order of the list.

        Args:
            x (T): The value to be inserted into the list.
        """
        if self.root is None:
            self.root = Node(x, None)
            return
        self._size += 1
        temp : Node = self.root
        prev : Node = None
        while temp and x > temp.val:
            prev = temp
            temp = temp.next

        if prev is None:
            self.root = Node(x, temp)
        else:
            prev.next = Node(x, temp)

    def search(self, x: T) -> Node:
        """
        Searches for a node with the given value in the sorted linked list.

        This method searches for a node with the value `x` in the sorted linked list. 
        If found, it returns the node; otherwise, it returns `None`.

        Args:
            x (T): The value to be searched in the list.

        Returns:
            Node: The node with the value `x` if found, otherwise `None`.
        """
        temp = self.root
        while temp:
            if temp.val == x:
                return temp
            temp = temp.next
        return None

    def delete(self, x: T) -> None:
        """
        Deletes a node with the given value from the sorted linked list.

        This method deletes the first occurrence of a node with the value `x` 
        from the sorted linked list. If no such node is found, the list remains unchanged.

        Args:
            x (T): The value of the node to be deleted from the list.
        """
        if self.root is None:
            return
        
        temp : Node = self.root
        prev : Node = None
        while temp is not None and x > temp.val:
            prev = temp
            temp = temp.next
        if temp is not None and x == temp.val:
            self._size -= 1
            if prev is not None:
                prev.next = temp.next
            else: # account for edge case where root is only Node
                # self.root = temp.next
                self.root = None
            
    def __len__(self):
        return self._size

    def __str__(self):
        s : List[str] = ['[']
        tmp : Node = self.root
        for i in range(self._size):
            if i != self._size - 1:
                s.append(str(tmp.val) + ", ")
                tmp = tmp.next
            else:
                s.append(str(tmp.val) + "]")

        return "".join(s)