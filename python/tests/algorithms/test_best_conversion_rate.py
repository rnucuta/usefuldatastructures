import unittest
from py_dsa.algorithms import blindDFS, Robot
from random import randint
import string
from py_dsa.algorithms.best_conversion_rate import best_conversion_rate
from py_dsa.datastructures import WeightedGraph
import random
import itertools
from parameterized import parameterized

class TestBestConversionRate(unittest.TestCase):
    def random_complete_graph(self, n, seed=None):
        if seed is not None:
            random.seed(seed)
        nodes = list(string.ascii_uppercase[:n])
        g = WeightedGraph()
        for u in nodes:
            g.add_node(u)
        for u in nodes:
            for v in nodes:
                if u == v:
                    g.add_edge(u, v, 1.0)
                else:
                    g.add_edge(u, v, random.uniform(0.1, 2.0))
        return g, nodes

    def brute_force_best_conversion(self, graph, source, destination):
        nodes = list(graph.get_nodes())
        n = len(nodes)
        node_idx = {node: i for i, node in enumerate(nodes)}
        max_product = 0.0

        def dfs(curr, visited, product):
            nonlocal max_product
            if curr == destination:
                max_product = max(max_product, product)
                return
            for neighbor, weight in graph.get_edges(curr).items():
                if neighbor not in visited:
                    dfs(neighbor, visited | {neighbor}, product * weight)

        dfs(source, {source}, 1.0)
        return max_product


    @parameterized.expand([(3,), (7,), (12,)])
    def test_random_graphs(self, graph_size: int):
        g, nodes = self.random_complete_graph(graph_size)
        source, destination = random.sample(nodes, 2)
        expected = self.brute_force_best_conversion(g, source, destination)
        actual = best_conversion_rate(g, source, destination)
        self.assertAlmostEqual(actual, expected, places=6,
            msg=f"Failed for n={graph_size}, source={source}, dest={destination}")
        