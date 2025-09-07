import unittest
from py_dsa.datastructures.lru_cache import LRUCache

class TestLRUCache(unittest.TestCase):
    def test_leetcode_case(self):
        lru = LRUCache(2)
        lru.put(1, 1)
        lru.put(2, 2)
        self.assertEqual(lru.get(1), 1)
        lru.put(3, 3)
        self.assertIsNone(lru.get(2))
        lru.put(4, 4)
        self.assertIsNone(lru.get(1)) 
        self.assertEqual(lru.get(3), 3)
        self.assertEqual(lru.get(4), 4)

if __name__ == "__main__":
    unittest.main()
