from typing import Generic, TypeVar, Dict

keyT = TypeVar('keyT')
valT = TypeVar('valT')

# TODO: add dependency onto normal LL

class Node:
    def __init__(self, key : keyT = None, val : valT = None, nextN : 'Node' = None, prev : 'Node'=None):
        self.key = key
        self.val = val
        self.next = nextN
        self.prev = prev

    def __str__(self):
        return "[key: {}, val:{}]".format(self.key, self.val)


# doubly linked list stores order of adding to the cache
# most recent at start, oldest at the end
class DoublyLinkedList(Generic[keyT, valT]):
    def __init__(self, capacity : int):
        self.dummyHead = Node()
        self.dummyTail = Node(prev = self.dummyHead)
        self.dummyHead.next = self.dummyTail
        self.capacity = capacity
        self.len = 0

    def add_head(self, node : Node) -> keyT:
        if self.len == self.capacity:
            #pop tail, insert head, return key popped
            temp_key : keyT = self.dummyTail.prev.key
            tail_node : Node = self.dummyTail.prev
            self.remove_node(tail_node)
            self.add_node(node)
            return temp_key

        self.add_node(node)
        return None

    def remove_node(self, node : Node) -> None:
        prev : Node = node.prev
        nextN : Node = node.next
        prev.next = nextN
        nextN.prev = prev
        self.len -= 1

    def add_node(self, node : Node) -> None:
        #adding to head
        node.next = self.dummyHead.next
        node.prev = self.dummyHead
        self.dummyHead.next.prev = node
        self.dummyHead.next = node
        self.len += 1

    def __str__(self):
        temp = self.dummyHead
        toPrint = ""
        while temp:
            toPrint += str(temp) + "\n"
            temp = temp.next
        return toPrint
            

    def get_head(self) -> keyT:
        if self.len == 0:
            return None
        return self.dummyHead.next.key

    def get_tail(self) -> keyT:
        if self.len == 0:
            return None
        return self.dummyHead.prev.key


class LRUCache:
    def __init__(self, capacity: int):
        self.order = DoublyLinkedList(capacity)
        #key to node
        self.location : Dict[keyT, Node] = {}

    def get(self, key: keyT) -> valT:
        # print(self.order)
        if key in self.location:
            # change node's accessing order
            node = self.location[key]
            self.order.remove_node(node)
            self.order.add_node(node)
            return node.val
        return None

    def put(self, key: keyT, value: valT) -> None:
        if key in self.location:
            # change node's accessing order
            node : Node = self.location[key]
            node.val = value
            self.order.remove_node(node)
            self.order.add_node(node)
        else:
            temp : Node = Node(key, value)
            self.location[key] = temp
            to_del : keyT = self.order.add_head(temp)
            if to_del is not None:
                del self.location[to_del]

    def __str__(self) -> str:
        return str(self.order)
    
    def __len__(self) -> int:
        return self.order.len

