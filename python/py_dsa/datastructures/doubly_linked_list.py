from typing import Generic, TypeVar, Optional, Callable
from abc import ABC

T = TypeVar("T", bound="AbstractNode")
NodeType = TypeVar("NodeType", bound="AbstractNode")

class AbstractNode(Generic[T], ABC):
    def __init__(
        self,
        next: Optional[T] = None,
        prev: Optional[T] = None,
    ):
        self.next = next
        self.prev = prev



class DoublyLinkedList(Generic[NodeType]):
    """A generic doubly linked list that can work with any node type.
    
    This implementation provides a flexible doubly linked list that can
    work with different node types, as long as the nodes have 'next' and 'prev'
    attributes that can be set to None or other nodes.
    """

    def __init__(self):
        """Initialize an empty doubly linked list."""
        self.head: AbstractNode = AbstractNode[NodeType]()
        self.tail: AbstractNode = AbstractNode[NodeType]()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def push_front(self, node: NodeType) -> None:
        """Add a node to the front of the list.
        
        Args:
            node: The node to add to the front.

        """
        node.next = self.head.next
        node.prev = self.head
        assert self.head.next is not None
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def push_back(self, node: NodeType) -> None:
        """Add a node to the back of the list.
        
        Args:
            node: The node to add to the back.

        """
        node.next = self.tail
        node.prev = self.tail.prev
        assert self.tail.prev is not None
        self.tail.prev.next = node
        self.tail.prev = node
        self.size += 1

    def pop_front(self) -> Optional[NodeType]:
        """Remove and return the first node from the list.
        
        Returns:
            The removed node, or None if the list is empty.

        """
        if self.size == 0:
            return None
        node = self.head.next
        assert node is not None
        self.remove(node) 
        return node

    def pop_back(self) -> Optional[NodeType]:
        """Remove and return the last node from the list.
        
        Returns:
            The removed node, or None if the list is empty.

        """
        if self.size == 0:
            return None
        node = self.tail.prev
        assert node is not None
        self.remove(node) 
        return node

    def remove(self, node: NodeType) -> None:
        """Remove a specific node from the list.
        
        Args:
            node: The node to remove.

        """
        assert node.prev is not None
        assert node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def move_to_front(self, node: NodeType) -> None:
        """Move a node to the front of the list.
        
        Args:
            node: The node to move to the front.

        """
        if node == self.head:
            return
        
        self.remove(node)
        self.push_front(node)

    def move_to_back(self, node: NodeType) -> None:
        """Move a node to the back of the list.
        
        Args:
            node: The node to move to the back.

        """
        if node == self.tail:
            return 
        
        self.remove(node)
        self.push_back(node)

    def is_empty(self) -> bool:
        """Check if the list is empty.
        
        Returns:
            True if the list is empty, False otherwise.

        """
        return self.size == 0

    def __len__(self) -> int:
        """Return the number of nodes in the list.
        
        Returns:
            The number of nodes in the list.
            
        """
        return self.size

    def __str__(self) -> str:
        """Return a string representation of the list.
        
        Returns:
            A string representation of the list.

        """
        if self.head is None:
            return "[]"
        
        result = "["
        current = self.head
        while current is not None:
            result += str(current)
            if current.next is not None:
                result += ", "
            current = current.next
        result += "]"
        return result