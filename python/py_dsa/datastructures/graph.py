import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Dict, Iterator

NODE_T = TypeVar("NODE_T")


class Graph(ABC, Generic[NODE_T]):
    """ABC for a graph type in this library. Can make a graph
    undirected or directed simply by adding edges both ways.
    """

    @abstractmethod
    def add_node(self, node: NODE_T) -> bool:  # noqa: D102
        pass

    @abstractmethod
    def add_edge(self, source: NODE_T, dest: NODE_T, weight: float = None) -> None:  # noqa: D102
        pass

    @abstractmethod
    def get_edges(self, source: NODE_T) -> Iterator[NODE_T]:  # noqa: D102
        pass

    @abstractmethod
    def get_nodes(self) -> Iterator[NODE_T]:  # noqa: D102
        pass

    @abstractmethod
    def get_idx(self, node: NODE_T) -> int:  # noqa: D102
        pass

    @abstractmethod
    def num_nodes(self) -> int:  # noqa: D102
        pass


class WeightedGraph(Graph):
    def __init__(self):
        self.G = defaultdict(dict)
        self.nodes = []
        self.idx_counter = 0
        self.idx_map = {}

    def add_node(self, node: NODE_T) -> bool:
        """Add a node to the graph.

        Args:
            node (NODE_T): The node to be added.

        Returns:
            bool: True if the node was added, False if it already exists.

        """
        if node in self.idx_map:
            return False
        self.nodes.append(node)
        self.idx_map[node] = self.idx_counter
        self.idx_counter += 1
        return True

    def add_edge(self, source: NODE_T, dest: NODE_T, weight: float = 1.0) -> None:
        """Add an edge between two nodes with an optional weight.

        Args:
            source (NODE_T): The source node.
            dest (NODE_T): The destination node.
            weight (float, optional): The weight of the edge. Defaults to 1.0.

        """
        self.add_node(source)
        self.add_node(dest)
        self.G[source][dest] = weight

    def get_nodes(self) -> List[NODE_T]:
        """Return a list of all nodes in the graph.

        Returns:
            List[NODE_T]: A list of nodes in the graph.

        """
        return self.nodes

    def get_edges(self, source: NODE_T) -> Dict[NODE_T, float]:
        """Get the edges connected to a given source node.

        Args:
            source (NODE_T): The source node.

        Returns:
            Dict[NODE_T, float]: A dictionary of edges connected to the source.

        """
        return self.G[source]

    def get_idx(self, node: NODE_T) -> int:
        """Get the index of a node.

        Args:
            node (NODE_T): The node.

        Returns:
            int: The index of the node, or -1 if not found.

        """
        return self.idx_map[node]

    def num_nodes(self) -> int:
        """Return the number of nodes in the graph.

        Returns:
            int: The number of nodes in the graph.

        """
        return len(self.nodes)


class UnweightedGraph(Graph):
    def __init__(self):
        self.G = defaultdict(set())
        self.nodes = []
        self.idx_counter = 0
        self.idx_map = {}

    def add_node(self, node: NODE_T) -> bool:
        """Add a node to the graph.

        Args:
            node (NODE_T): The node to be added.

        Returns:
            bool: True if the node was added, False if it already exists.

        """
        if node in self.idx_map:
            return False
        self.nodes.append(node)
        self.idx_map[node] = self.idx_counter
        self.idx_counter += 1
        return True

    def add_edge(self, source: NODE_T, dest: NODE_T) -> None:
        """Add an edge between two nodes.

        Args:
            source (NODE_T): The source node.
            dest (NODE_T): The destination node.

        """
        self.add_node(source)
        self.add_node(dest)
        self.G[source].add(dest)

    def get_nodes(self) -> List[NODE_T]:
        """Return a list of all nodes in the graph.

        Returns:
            List[NODE_T]: A list of nodes in the graph.

        """
        return self.nodes

    def get_edges(self, source: NODE_T) -> set[NODE_T]:
        """Get the edges connected to a given source node.

        Args:
            source (NODE_T): The source node.

        Returns:
            set[NODE_T]: A set of nodes connected to the source.

        """
        return self.G[source]

    def get_idx(self, node: NODE_T) -> int:
        """Get the index of a node.

        Args:
            node (NODE_T): The node.

        Returns:
            int: The index of the node, or -1 if not found.

        """
        return self.idx_map[node]

    def num_nodes(self) -> int:
        """Return the number of nodes in the graph.

        Returns:
            int: The number of nodes in the graph.

        """
        return len(self.nodes)


class MatchingGraph(Graph):
    def __init__(self, source: NODE_T, sink: NODE_T):
        self.G = defaultdict(lambda: defaultdict(int))
        self.F = defaultdict(lambda: defaultdict(int))
        self.nodes = set()
        self._source = source
        self._sink = sink

    def reset_residual_graph(self) -> None:
        """Reset the residual graph to its initial state."""
        self.F = defaultdict(lambda: defaultdict(int))

    def get_source(self) -> NODE_T:
        """Return the source node of the matching graph.

        Returns:
            NODE_T: The source node.

        """
        return self._source

    def get_sink(self) -> NODE_T:
        """Return the sink node of the matching graph.

        Returns:
            NODE_T: The sink node.

        """
        return self._sink

    def add_edge(self, u: NODE_T, v: NODE_T, w: int = 1) -> None:
        """Add an edge between two nodes with a specified weight.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.
            w (int, optional): The weight of the edge. Defaults to 1.

        """
        self.G[u][v] = w
        self.nodes.add(v)
        self.nodes.add(u)

    def add_node(self, u: NODE_T) -> None:
        """Add a node to the graph.

        Args:
            u (NODE_T): The node to be added.

        """
        self.G[u] = defaultdict(int)
        self.nodes.add(u)

    def get_edges(self, u: NODE_T) -> Dict[NODE_T, int]:
        """Get the edges connected to a given node.

        Args:
            u (NODE_T): The node.

        Returns:
            Dict[NODE_T, int]: A dictionary of edges connected to the node.

        """
        return self.G[u]

    def get_residual_edges(self, u: NODE_T) -> Dict[NODE_T, int]:
        """Get the residual edges connected to a given node.

        Args:
            u (NODE_T): The node.

        Returns:
            Dict[NODE_T, int]: A dictionary of residual edges connected to the node.

        """
        return self.F[u]

    def get_nodes(self) -> Iterator[NODE_T]:
        """Return a iter of all nodes in the graph.

        Returns:
            Iterator[NODE_T]: A list of nodes in the graph.

        """
        return iter(self.G.keys())

    def get_idx(self, node: NODE_T) -> int:
        """Get the index of a node.

        Args:
            node (NODE_T): The node.

        Returns:
            int: The index of the node, or -1 if not found.

        """
        idx = 0
        G_iter = iter(self.G)
        try:
            while node != next(G_iter):
                idx += 1
        except StopIteration:
            return -1
        return idx

    def get_residual_nodes(self) -> Iterator[NODE_T]:
        """Return an iterator over the residual nodes.

        Returns:
            Iterator[NODE_T]: An iterator over the residual nodes.

        """
        return iter(self.F.keys())

    def edge_exists(self, u: NODE_T, v: NODE_T) -> bool:
        """Check if an edge exists between two nodes.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.

        Returns:
            bool: True if the edge exists, False otherwise.

        """
        if v not in self.G[u] or not self.G[u][v]:
            return False
        return True

    def residual_edge_exists(self, u: NODE_T, v: NODE_T) -> bool:
        """Check if a residual edge exists between two nodes.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.

        Returns:
            bool: True if the residual edge exists, False otherwise.

        """
        if v not in self.F[u] or not self.F[u][v]:
            return False
        return True

    def get_edge_weight(self, u: NODE_T, v: NODE_T) -> float:
        """Get the weight of an edge between two nodes.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.

        Returns:
            float: The weight of the edge, or 0 if it does not exist.

        """
        return self.G[u][v] if self.edge_exists(u, v) else 0

    def get_residual_edge_weight(self, u: NODE_T, v: NODE_T) -> float:
        """Get the weight of a residual edge between two nodes.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.

        Returns:
            float: The weight of the residual edge, or 0 if it does not exist.

        """
        return self.F[u][v] if self.residual_edge_exists(u, v) else 0

    def update_residual_edge_weight(self, u: NODE_T, v: NODE_T, w: float) -> None:
        """Update the weight of a residual edge.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.
            w (float): The new weight of the residual edge.

        """
        self.F[u][v] = w

    def preliminary_assignment(self, u: NODE_T, v: NODE_T, w: int = 1) -> None:
        """Make a preliminary assignment for a bipartite graph.

        Args:
            u (NODE_T): The first node.
            v (NODE_T): The second node.
            w (int, optional): The weight of the assignment. Defaults to 1.

        """
        # only for bipartite graphs to add initial vlow
        self.F[self._source][u] += w
        self.F[u][v] += w
        self.F[v][self._sink] += w

    # TODO: consider using networkx as backing implementation for MatchingGraph so
    # so this function doesnt have as much overhead?
    def visualize(self, fname: str = "test.png") -> None:
        """Visualize the graph and save it to a file.

        Args:
            fname (str, optional): The filename to save the visualization. Defaults to 'test.png'.

        """
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
        layers["source"].append(self._source)
        layers["sink"].append(self._sink)

        for u in self.G:
            if u != self._source and u != self._sink:
                if any(v == self._sink for v in self.G[u]):
                    layers["sink_layer"].append(u)
                elif any(v == self._source for v in self.G[u]):
                    layers["source_layer"].append(u)
                else:
                    layers["intermediate"].append(u)

        # Calculate canvas size
        num_layers = max(len(layers["intermediate"]), len(layers["sink_layer"]))
        height = max(8, num_layers * 0.5)

        plt.figure(figsize=(10, height))

        pos = {}
        layer_spacing = 2
        node_spacing = 1

        pos[self._source] = (-layer_spacing, 0)

        for i, node in enumerate(layers["intermediate"]):
            pos[node] = (0, i * node_spacing)

        for i, node in enumerate(layers["sink_layer"]):
            pos[node] = (layer_spacing, i * node_spacing)

        pos[self._sink] = (layer_spacing * 2, 0)

        nx.draw_networkx_nodes(
            nx_graph, pos, node_color="lightblue", node_size=700, edgecolors="black"
        )

        for u, v in nx_graph.edges():
            if v in self.F[u] and self.F[u][v] > 0:
                nx.draw_networkx_edges(
                    nx_graph,
                    pos,
                    edgelist=[(v, u)],
                    connectionstyle="arc3,rad=0.2",
                    arrowstyle="->",
                    arrowsize=20,
                    edge_color="red",
                )
            else:
                nx.draw_networkx_edges(
                    nx_graph,
                    pos,
                    edgelist=[(u, v)],
                    connectionstyle="arc3,rad=0",
                    arrowstyle="->",
                    arrowsize=20,
                    edge_color="gray",
                )

        nx.draw_networkx_labels(nx_graph, pos, font_size=10, font_color="black")

        plt.title("Bipartite Graph Visualization")
        plt.axis("off")
        plt.savefig(fname)
        plt.close()

    def num_nodes(self) -> int:
        """Get total number of nodes in G"""
        return len(self.nodes)
