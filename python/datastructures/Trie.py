'''
'''

from collections import deque

class TrieNode:
    def __init__(self, word=None):
        self.children = {}
        self.word = word
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.word = word
        curr.count += 1

    def countWordsEqualTo(self, word: str) -> int:
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
        def dfs(node, idx):
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