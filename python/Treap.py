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

class Treap(Generic[T]):
    """
    A class representing a Treap. A Treap maintains amortized
    O(log(n)) time insert, search, and delete operations.

    Attributes:
        root (TreapNode): A reference to the root node in the Treap.
    """
    def __init__(self):
        self.root = None
        self._size = 0

    def _rotateLeft(self, node: TreapNode) -> TreapNode:
        left = node.left
        if left is None:
            return node
        node.left = left.right
        if left.right:
            left.right.parent = node
        left.right = node

        left.parent = node.parent
        if node.parent:
            if node.parent.left == node:
                node.parent.left = left
            else:
                node.parent.right = left
        else:
            self.root = left
        node.parent = left
        
        return left

    def _rotateRight(self, node: TreapNode) -> TreapNode:
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def _transplant(self, u: TreapNode, v: TreapNode) -> None:
        pass

    def insert(self, x: T) -> None:
        """
        Inserts a new node with the given value into the Treap.

        Args:
            x (T): The value to be inserted into the Treap.
        """
        self.root = self._insert(self.root, x)
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

    def _insert(self, node: TreapNode, x: T) -> TreapNode:
        if node is None:
            return TreapNode(x)
        if node.val > x:
            node.left = self._insert(node.left, x)
            if node.left.priority > node.priority:
                node = self._rotateRight(node)
        else:
            node.right = self._insert(node.right, x)
            if node.right.priority > node.priority:
                node = self._rotateLeft(node)
        return node

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
    
