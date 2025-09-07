from typing import Union  
from py_dsa.datastructures import WeightedGraph
from functools import cache

def best_conversion_rate(graph: WeightedGraph, source: str, destination: str) -> float:
    """Given a graph (type WeightedGraph) of potential currency conversions, 
    and a source and destination currency, find the best achievable conversion
    rate from source to destination. Assume graph is a complete graph, structured
    st nodes have loops to themselves with weight 1, and you cannot visit the same 
    node twice/have a cycle.
    This is an NP-hard problem. Brute force TC is factorial, below solution is 
    O(n^2*2^n). Analogous to the travelling salesman problem."""

    @cache
    def dfs(node: str, visited: int) -> float:
        if node == destination:
            return 1
        node_idx = graph.get_idx(node)
        visited |= 1 << node_idx
        result = 0
        for neighbor, weight in graph.get_edges(node).items():
            neighbor_idx = graph.get_idx(neighbor)
            if not (visited & (1 << neighbor_idx)):
                result = max(result, weight * dfs(neighbor, visited))
        return result
    return dfs(source, 0)


