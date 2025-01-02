from dataclasses import dataclass
from typing import Generic, TypeVar, List
import random

valT = TypeVar('valT')
keyT = TypeVar('keyT')

@dataclass
class TreapDictNode:
    """
    A class representing a node in a Treap.

    Attributes:
        val (T): The value stored in the node.
        left (TreapNode): A reference to the left node in the Treap.
        right (TreapNode): A reference to the right node in the Treap.
        priority (int): Priority of the node in the Treap.
    """
    key: keyT
    val: valT
    left: 'TreapDictNode' = None
    right: 'TreapDictNode' = None
    priority: int = random.randint(0, 100000)

class TreeMap(Generic[valT, keyT]):
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
        pass

    def _rotateRight(self, node: TreapNode) -> TreapNode:
        pass

    def _transplant(self, u: TreapNode, v: TreapNode) -> None:
        pass

    def insert(self, key: keyT, val: valT) -> None:
        """
        Inserts a new node with the given value into the Treap.

        Args:
            x (T): The value to be inserted into the Treap.
        """
        self.root = self._insert(self.root, key, val)
        self._size += 1

    def delete(self, key: keyT) -> None:
        """
        Deletes a node with the given value from the Treap.
        """
        if self._size == 0:
            return None

    def search(self, key: keyT) -> TreapNode:
        """
        Searches for a node with the given value in the Treap.
        """
        tmp : TreapNode = self.root
        while tmp and tmp.key != key:
            if key < tmp.key:
                tmp = tmp.left
            else:
                tmp = tmp.right
        return tmp.val

    def _insert(self, node: TreapNode, x: T) -> TreapNode:
        if node is None:
            pass

    def treapMax(self) -> TreapNode:
        tmp : TreapNode = self.root
        while tmp.right:
            tmp = tmp.right
        return tmp

    def treapMin(self) -> TreapNode:
        tmp : TreapNode = self.root
        while tmp.left:
            tmp = tmp.left
        return tmp

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
    
