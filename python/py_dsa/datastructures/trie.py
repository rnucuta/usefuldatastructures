"""test"""

from collections import deque


class TrieNode:
    """Represents a single node in the Trie."""

    def __init__(self, word: str = None):
        """Initializes a TrieNode with optional word and initializes children and count."""
        self.children = {}
        self.word = word
        self.count = 0


class Trie:
    """Represents the Trie data structure."""

    def __init__(self):
        """Initializes the Trie with a root TrieNode."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the Trie.

        Args:
            word (str): The word to insert.

        """
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.word = word
        curr.count += 1

    def countWordsEqualTo(self, word: str) -> int:
        """Counts the number of times a word appears in the Trie.

        Args:
            word (str): The word to count.

        Returns:
            int: The count of the word in the Trie.

        """
        n = len(word)
        dq = deque([(self.root, 0)])

        while dq:
            t, idx = dq.pop()
            if idx == n:
                if t.word is not None:
                    return t.count
                continue
            elif word[idx] == ".":
                for c in t.children:
                    dq.append((t.children[c], idx + 1))
            elif word[idx] in t.children:
                dq.append((t.children[word[idx]], idx + 1))

        return 0

    def countWordsStartingWith(self, prefix: str) -> int:
        """Counts the number of words starting with a given prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            int: The count of words starting with the prefix.

        """
        n = len(prefix)
        dq = deque([(self.root, 0)])
        count = 0

        while dq:
            t, idx = dq.pop()
            if idx == n:
                count += t.count
                dq.extend([(child, idx) for child in t.children.values()])
                continue
            elif prefix[idx] == ".":
                for c in t.children:
                    dq.append((t.children[c], idx + 1))
            elif prefix[idx] in t.children:
                dq.append((t.children[prefix[idx]], idx + 1))

        return count

    def erase(self, word: str) -> None:
        """Removes a word from the Trie.

        Args:
            word (str): The word to remove.

        """

        def dfs(node: TrieNode, idx: int) -> bool:
            if idx == len(word):
                if node.word is not None:
                    node.count -= 1
                    if node.count == 0:
                        node.word = None
                return node.count == 0 and not node.children

            c = word[idx]
            if c in node.children:
                should_delete = dfs(node.children[c], idx + 1)
                if should_delete:
                    del node.children[c]
                return not node.children and node.word is None

            return False

        dfs(self.root, 0)
