from dataclasses import dataclass
from typing import Generic, TypeVar, List
import random

T = TypeVar('T')

@dataclass
class TreapNode:
    """
    A class representing a node in a Treap.

    Attributes:
        val (T): The value stored in the node.
        left (TreapNode): A reference to the left node in the Treap.
        right (TreapNode): A reference to the right node in the Treap.
        priority (int): Priority of the node in the Treap.
    """
    val: T
    left: 'TreapNode' = None
    right: 'TreapNode' = None
    priority: int = random.randint(0, 100000)
    parent: 'TreapNode' = None
    size : int = 1

class Treap(Generic[T]):
    """
    A class representing a Treap. A Treap maintains amortized
    O(log(n)) time insert, search, and delete operations.

    Attributes:
        root (TreapNode): A reference to the root node in the Treap.
    """
    def __init__(self, root : TreapNode = None):
        self.root = root

    def _rotateLeft(self, node: TreapNode) -> TreapNode:
        """
        Rotates the Treap to the left around the given node.

        This method adjusts the Treap structure by rotating the node to the 
        left, updating the parent and child relationships accordingly. 
        It returns the new root of the rotated subtree.

        Args:
            node (TreapNode): The node around which the Treap is rotated to the left.

        Returns:
            TreapNode: The new root of the rotated subtree.
        """
        child : TreapNode = node.right
        node.right = child.left
        if child.left:
            child.left.parent = node
        child.parent = node.parent
        # initial rotation is complete
        # fix parent pointers depending on 
        # if node is root or left/right child
        if node.parent is None:
            self.root = child
        elif node == node.parent.left:
            node.parent.left = child
        else:
            node.parent.right = child
        # make child's left child the node
        child.left = node
        # make child the node's parent
        node.parent = child

    def _rotateRight(self, node: TreapNode) -> TreapNode:
        child: TreapNode = node.left
        node.left = child.right
        if child.right:
            child.right.parent = node
        child.parent = node.parent
        if node.parent is None:
            self.root = child
        elif node == node.parent.right:
            node.parent.right = child
        else:
            node.parent.left = child
        child.right = node
        node.parent = child

    def _transplant(self, u: TreapNode, v: TreapNode) -> None:
        pass

    def insert(self, z: T) -> None:
        """
        Inserts a new node with the given value into the Treap.
        Iterative choice to avoid stack overflow limit.

        Args:
            x (T): The value to be inserted into the Treap.
        """
        z : TreapNode = TreapNode(z)
        y : TreapNode = None
        x : TreapNode = self.root
        while x:
            y = x
            if z.val < x.val:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y is None:
            self.root = z
        elif z.val < y.val:
            y.left = z
        else:
            y.right = z

        # Restore the heap property by rotating up if needed
        while z.parent and z.priority > z.parent.priority:
            if z == z.parent.left:
                self._rotateRight(z.parent)
            else:
                self._rotateLeft(z.parent)

        self._size += 1

    def delete(self, x: T) -> None:
        """
        Deletes a node with the given value from the Treap.
        """
        if self._size == 0:
            return None

    def search(self, x: T) -> TreapNode:
        """
        Searches for a node with the given value in the Treap.
        """
        tmp : TreapNode = self.root
        while tmp and tmp.val != x:
            if x < tmp.val:
                tmp = tmp.left
            else:
                tmp = tmp.right
        return tmp

    def treapMax(self) -> TreapNode:
        tmp : TreapNode = self.root
        while tmp.right:
            tmp = tmp.right
        return tmp.val

    def treapMin(self) -> TreapNode:
        tmp : TreapNode = self.root
        while tmp.left:
            tmp = tmp.left
        return tmp.val

    def preorder(self) -> List[T]:
        res = []
        def _preorder(node: TreapNode) -> None:
            if node is None:
                return
            res.append(node.val)
            _preorder(node.left)
            _preorder(node.right)
        _preorder(self.root)
        return res

    def inorder(self) -> List[T]:
        res = []
        def _inorder(node: TreapNode) -> None:
            if node is None:
                return
            _inorder(node.left)
            res.append(node.val)
            _inorder(node.right)
        _inorder(self.root)
        return res

    def postorder(self) -> List[T]:
        res = []
        def _postorder(node: TreapNode) -> None:
            if node is None:
                return
            _postorder(node.left)
            _postorder(node.right)
            res.append(node.val)
        _postorder(self.root)
        return res

    def __str__(self) -> str:
        return str([str(x.val) for x in self.inorder()])
    
    def __len__(self) -> int:
        return self._size
    
