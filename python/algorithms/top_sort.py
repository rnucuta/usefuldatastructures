from abc import ABC, abstractmethod
from collections import defaultdict, deque
from typing import List
# can make this undirected or directed 
# simply by adding edges both ways
class Graph(ABC):
    @abstractmethod
    def add_node(self, node):
        pass

    @abstractmethod
    def add_edge(self, source, dest, weight=None):
        pass

    @abstractmethod
    def get_edges(self, source):
        pass

    @abstractmethod
    def get_nodes(self):
        pass

    @abstractmethod
    def get_idx(self, node):
        pass

    @abstractmethod
    def num_nodes(self):
        pass

class WeightedGraph(Graph):
    def __init__(self):
        self.G = defaultdict(dict)
        self.nodes = []
        self.idx_counter = 0
        self.idx_map = {}
    
    def add_node(self, node):
        if node in self.idx_map:
            return False
        self.nodes.append(node)
        self.idx_map[node] = self.idx_counter
        self.idx_counter += 1
        return True

    def add_edge(self, source, dest, weight):
        self.add_node(source)
        self.add_node(dest)
        self.G[source][dest] = weight

    def get_nodes(self):
        return self.nodes
    
    def get_edges(self, source):
        return self.G[source]
    
    def get_idx(self, node):
        return self.idx_map[node]

    def num_nodes(self):
        return len(self.nodes)

class UnweightedGraph(Graph):
    def __init__(self):
        self.G = defaultdict(set())
        self.nodes = []
        self.idx_counter = 0
        self.idx_map = {}
    
    def add_node(self, node):
        if node in self.idx_map:
            return False
        self.nodes.append(node)
        self.idx_map[node] = self.idx_counter
        self.idx_counter += 1
        return True

    def add_edge(self, source, dest):
        self.add_node(source)
        self.add_node(dest)
        self.G[source].add(dest)
    
    def get_nodes(self):
        return self.nodes

    def get_edges(self, source):
        return self.G[source]
    
    def get_idx(self, node):
        return self.idx_map[node]
    
    def num_nodes(self):
        return len(self.nodes)

# Khan's algorithm
# returns list of nodes if valid
# otherwise empty list
def top_sort(G):
    n = G.num_nodes()
    indegree = [0] * n
    for u in G.get_nodes():
        for v in G.get_edges(u):
            indegree[G.get_idx(v)] += 1
    
    dq = deque()

    for i in range(n):
        if not indegree[i]:
            dq.append(i)
        
    top_sorted_idxs = []
    while dq:
        u_idx = dq.popleft()
        top_sorted_idxs.append(u_idx)

        u_val = G.get_nodes()[u_idx]
        for v_val in G.get_edges(u_val):
            v_idx = G.get_idx(v_val)
            indegree[v_idx] -= 1

            if not indegree[v_idx]:
                dq.append(v_idx)

    # Check for cycle
    if len(top_sorted_idxs) != n:
        return []
    return [G.get_nodes()[idx] for idx in top_sorted_idxs]

# detect cycle in undirected graph
def validTree(self, n: int, edges: List[List[int]]) -> bool:
        visited = set()
        G = defaultdict(set)
        for a, b in edges:
            G[a].add(b)
            G[b].add(a)
        
        def dfs(u, parent):
            # print(u, parent)
            visited.add(u)
            for v in G[u]:
                if v not in visited:
                    if not dfs(v, u):
                        # print(v, u)
                        return False
                # cycle detected
                # if you have visited a node already
                # in your adjacency list that isnt your
                # parent, then at some point another branch of 
                # dfs has visited that point
                # meaning that there is a cycle
                elif v != parent:
                    return False

            return True

        if dfs(0, None):
            # print(len(visited))
            return len(visited) == n
        return False


def is_bipartite(g_l) -> bool:
    """
    Test if a given graph is bipartite using BFS

    param: g_l: dict of adjacency lists of the graph
    output: bool, True if the graph is bipartite, False otherwise
    """
    node_colors = {k: None for k in g_l}
    # perform BFS for each connected component
    for starting_node in g_l:
        if node_colors[starting_node] is not None:
            continue
        # see if any neighbor is already set to try to set the color 
        # correctly initially
        if g_l[starting_node]:
            for neighbor in g_l[starting_node]:
                if node_colors[neighbor] is not None:
                    node_colors[starting_node] = node_colors[neighbor] ^ 1
                    break
        # if still not set, then set it to color 0
        if node_colors[starting_node] is None:
            node_colors[starting_node] = 0
        queue = deque([starting_node])
        # BFS to check if the graph is bipartite
        # dont need to check for visited nodes 
        # as they are being colored
        while queue:
            node = queue.popleft()
            for neighbor in g_l[node]:
                if node_colors[neighbor] is None:
                    node_colors[neighbor] = node_colors[node] ^ 1
                    queue.append(neighbor)
                elif node_colors[neighbor] == node_colors[node]:
                    return False
    return True
