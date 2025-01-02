# https://leetcode.com/problems/valid-arrangement-of-pairs

from typing import List
from collections import defaultdict

def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
    # eularian path - path that visits every edge once
    # eularian circuit - eularian path that ends at start node

    # requirements: for eularian path to exist
    # at most one vertex has outdegree - indegree = 1
    # and one vertex has indegree - outdegree = 1
    # and rest outdegree == indegree

    # start at node with outdegree - indegree = 1
    # end node indegree - outdegree = 1
    # https://www.youtube.com/watch?v=8MpoO2zA2l4
    G = defaultdict(list)
    out_degree = defaultdict(int)
    in_degree = defaultdict(int)
    for u, v in pairs:
        G[u].append(v)
        out_degree[u] += 1
        in_degree[v] += 1
    
    starting_node = None
    for k in out_degree:
        if out_degree[k] - in_degree[k] == 1:
            starting_node = k
            break
        if not starting_node and out_degree[k] - in_degree[k] == -1:
            starting_node = k
    
    if starting_node is None:
        starting_node = pairs[0][0]

    result = []

    # algo is basically dfs
    # except you need to keep track
    # of visited edges not visited nodes
    def dfs(start):
        while G[start]:
            dfs(G[start].pop())
        if result:
            result.append([start, result[-1][0]])
        else:
            result.append([start, None])

    dfs(starting_node)
        
    result.reverse()
    result.pop()

    return result