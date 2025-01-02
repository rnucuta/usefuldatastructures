from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx

class matchingGraph:
    def __init__(self, source, sink):
        self.G = defaultdict(lambda: defaultdict(int))
        self.F = defaultdict(lambda: defaultdict(int))
        self._source = source
        self._sink = sink

    def reset_residual_graph(self):
        self.F = defaultdict(lambda: defaultdict(int))

    def get_source(self):
        return self._source
    
    def get_sink(self):
        return self._sink

    def add_edge(self, u, v, w = 1):
        self.G[u][v] = w

    def add_node(self, u):
        self.G[u] = defaultdict(int)

    def get_edges(self, u):
        return self.G[u]
    
    def get_residual_edges(self, u):
        return self.F[u]
    
    def get_nodes(self):
        return iter(self.G.keys())

    def get_residual_nodes(self):
        return iter(self.F.keys())

    def edge_exists(self, u, v):
        if v not in self.G[u] or not self.G[u][v]:
            return False
        return True
    
    def residual_edge_exists(self, u, v):
        if v not in self.F[u] or not self.F[u][v]:
            return False
        return True
    
    def get_edge_weight(self, u, v):
        return self.G[u][v] if self.edge_exists(u, v) else 0

    def get_residual_edge_weight(self, u, v):
        return self.F[u][v] if self.residual_edge_exists(u, v) else 0
    
    def update_residual_edge_weight(self, u, v, w):
        self.F[u][v] = w

    def preliminary_assignment(self, u, v, w = 1):
        # only for bipartite graphs to add initial vlow
        self.F[self._source][u] += w
        self.F[u][v] += w
        self.F[v][self._sink] += w
    
    def visualize(self, fname = 'test.png'):
        nx_graph = nx.DiGraph()

        # add nodes and edges to graph
        for u in self.G:
            for v, w in self.G[u].items():
                if w > 0:
                    nx_graph.add_edge(u, v)

        if self._source not in nx_graph:
            nx_graph.add_node(self._source)
        if self._sink not in nx_graph:
            nx_graph.add_node(self._sink)

        # Use a bipartite layout
        layers = defaultdict(list)
        layers['source'].append(self._source)
        layers['sink'].append(self._sink)

        for u in self.G:
            if u != self._source and u != self._sink:
                if any(v == self._sink for v in self.G[u]):
                    layers['sink_layer'].append(u)
                elif any(v == self._source for v in self.G[u]):
                    layers['source_layer'].append(u)
                else:
                    layers['intermediate'].append(u)

        # Calculate canvas size
        num_layers = max(len(layers['intermediate']), len(layers['sink_layer']))
        height = max(8, num_layers * 0.5)

        plt.figure(figsize=(10, height))

        pos = {}
        layer_spacing = 2
        node_spacing = 1

        pos[self._source] = (-layer_spacing, 0)

        for i, node in enumerate(layers['intermediate']):
            pos[node] = (0, i * node_spacing)

        for i, node in enumerate(layers['sink_layer']):
            pos[node] = (layer_spacing, i * node_spacing)

        pos[self._sink] = (layer_spacing * 2, 0)

        nx.draw_networkx_nodes(nx_graph, pos, node_color='lightblue', node_size=700, edgecolors='black')
        
        for u, v in nx_graph.edges():
            if v in self.F[u] and self.F[u][v] > 0:
                nx.draw_networkx_edges(nx_graph, pos, edgelist=[(v, u)], connectionstyle='arc3,rad=0.2', arrowstyle='->', arrowsize=20, edge_color='red')
            else:
                nx.draw_networkx_edges(nx_graph, pos, edgelist=[(u, v)], connectionstyle='arc3,rad=0', arrowstyle='->', arrowsize=20, edge_color='gray')

        nx.draw_networkx_labels(nx_graph, pos, font_size=10, font_color='black')

        plt.title("Bipartite Graph Visualization")
        plt.axis("off")
        plt.savefig(fname)
        plt.close()


class MaxFlow:
    def __init__(self, MG):
        self.MG = MG

    def find_path(self):
        # find a simple path from s to t
        # using bfs
        # visited = [False]*len(G)
        visited = set()
        # parent = [-1]*len(G)
        parent = {}
        queue = deque([self.MG.get_source()])
        # visited[s] = True
        visited.add(self.MG.get_source())

        while queue:
            u = queue.popleft()
            # push forward on edges with excess capacity
            for v in self.MG.get_edges(u):
                if v == u or not self.MG.edge_exists(u, v):
                    continue
                residual = self.MG.get_edge_weight(u, v) - self.MG.get_residual_edge_weight(u, v)
                if v not in visited and residual > 0:
                    queue.append(v)
                    # visited[v] = True
                    visited.add(v)
                    parent[v] = u
                    if v == self.MG.get_sink():
                        return self.reconstruct_path(parent)
            # push backwards on edges already carrying flow (positive)
            # to u (current node) in residual graph (so really u to v 
            # in real graph) to opposite direction
            # In other words, allows us to redirect flow that might 
            # have been sent on a suboptimal path
            for v in self.MG.get_residual_nodes():
                if not v == u and v not in visited and self.MG.residual_edge_exists(v, u) and self.MG.get_residual_edge_weight(v, u) > 0:
                    # print(u, v)
                    queue.append(v)
                    # visited[v] = True
                    visited.add(v)
                    parent[v] = u # swap parent
                    if v == self.MG.get_sink():
                        return self.reconstruct_path(parent)
        return None

    # get path from BFS by traversing through parents array
    def reconstruct_path(self, parent):
        path = []
        v = self.MG.get_sink()
        while v != self.MG.get_source():
            u = parent[v]
            path.append((u, v))
            v = u
        path.reverse()
        return path

    def bottleneck(self, path):
        # min residual capacity of any edge on path
        # path is a simple path from s to t
        b = float('inf')
        for u, v in path:
            if self.MG.edge_exists(u, v): # Forward edge
                b = min(b, self.MG.get_edge_weight(u, v) - self.MG.get_residual_edge_weight(u, v))
            else:  # Backward edge
                b = min(b, self.MG.get_residual_edge_weight(v, u))
        # if b < 0:
        #     print(b)
        return b
    
    # update residual graph with bottleneck
    def augment(self, path, b):
        # print(path)
        # augment flow along path by b
        for u, v in path:
            F_uv = self.MG.get_residual_edge_weight(u, v)
            if self.MG.edge_exists(u, v): # Forward edge
                self.MG.update_residual_edge_weight(u, v, F_uv + b)
            else: # Backward edge
                # print(u, v)
                # print(F[v][u])
                self.MG.update_residual_edge_weight(u, v, F_uv - b)

    def max_flow_val(self):                    
        path = self.find_path()
        i = 0
        while path:
            if i == 5:
                break
            # print("step",  i)
            i += 1
            b = self.bottleneck(path)
            print("b", b, "i", i)
            self.augment(path, b)
            path = self.find_path()

        max_flow_value = sum(
            self.MG.get_residual_edge_weight(self.MG.get_source(), v) 
            for v in self.MG.get_edges(self.MG.get_source())
        )
        return max_flow_value
        