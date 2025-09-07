import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Dict, Iterator, Set

NODE_T = TypeVar("NODE_T")


class GraphError(Exception):
    """Base exception for graph operations."""
    pass


class NodeNotFoundError(GraphError):
    """Raised when attempting to access a node that doesn't exist."""
    pass


class EdgeNotFoundError(GraphError):
    """Raised when attempting to access an edge that doesn't exist."""
    pass


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


class BaseGraph(Graph[NODE_T]):
    """Base implementation providing common node management functionality.
    
    This class handles the boilerplate of node indexing, storage, and basic
    validation, allowing subclasses to focus on their specific edge storage
    and retrieval logic.
    """
    
    def __init__(self):
        self._nodes: List[NODE_T] = []
        self._node_to_idx: Dict[NODE_T, int] = {}
        self._idx_counter = 0
    
    def add_node(self, node: NODE_T) -> bool:
        """Add a node to the graph.

        Args:
            node (NODE_T): The node to be added.

        Returns:
            bool: True if the node was added, False if it already exists.

        Raises:
            TypeError: If node is None.
        """
        if node is None:
            raise TypeError("Node cannot be None")
            
        if node in self._node_to_idx:
            return False
            
        self._nodes.append(node)
        self._node_to_idx[node] = self._idx_counter
        self._idx_counter += 1
        return True

    def get_nodes(self) -> List[NODE_T]:
        """Return a list of all nodes in the graph.

        Returns:
            List[NODE_T]: A list of nodes in the graph.
        """
        return self._nodes.copy()

    def get_idx(self, node: NODE_T) -> int:
        """Get the index of a node.

        Args:
            node (NODE_T): The node.

        Returns:
            int: The index of the node.

        Raises:
            NodeNotFoundError: If the node doesn't exist in the graph.
        """
        if node not in self._node_to_idx:
            raise NodeNotFoundError(f"Node {node} not found in graph")
        return self._node_to_idx[node]

    def num_nodes(self) -> int:
        """Return the number of nodes in the graph.

        Returns:
            int: The number of nodes in the graph.
        """
        return len(self._nodes)
    
    def has_node(self, node: NODE_T) -> bool:
        """Check if a node exists in the graph.

        Args:
            node (NODE_T): The node to check.

        Returns:
            bool: True if the node exists, False otherwise.
        """
        return node in self._node_to_idx
    
    def _validate_nodes_exist(self, *nodes: NODE_T) -> None:
        """Validate that all given nodes exist in the graph.

        Args:
            *nodes: Variable number of nodes to validate.

        Raises:
            NodeNotFoundError: If any node doesn't exist.
        """
        for node in nodes:
            if not self.has_node(node):
                raise NodeNotFoundError(f"Node {node} not found in graph")


class WeightedGraph(BaseGraph[NODE_T]):
    """A graph with weighted edges stored as adjacency dictionaries."""
    
    def __init__(self):
        super().__init__()
        self._adjacency: Dict[NODE_T, Dict[NODE_T, float]] = defaultdict(dict)

    def add_edge(self, source: NODE_T, dest: NODE_T, weight: float = 1.0) -> None:
        """Add an edge between two nodes with an optional weight.

        Args:
            source (NODE_T): The source node.
            dest (NODE_T): The destination node.
            weight (float, optional): The weight of the edge. Defaults to 1.0.

        Raises:
            TypeError: If weight is not a number.
        """
        if not isinstance(weight, (int, float)):
            raise TypeError("Edge weight must be a number")
            
        self.add_node(source)
        self.add_node(dest)
        self._adjacency[source][dest] = weight

    def get_edges(self, source: NODE_T) -> Dict[NODE_T, float]:
        """Get the edges connected to a given source node.

        Args:
            source (NODE_T): The source node.

        Returns:
            Dict[NODE_T, float]: A dictionary of edges connected to the source.

        Raises:
            NodeNotFoundError: If the source node doesn't exist.
        """
        self._validate_nodes_exist(source)
        return self._adjacency[source].copy()
    
    def get_edge_weight(self, source: NODE_T, dest: NODE_T) -> float:
        """Get the weight of an edge between two nodes.

        Args:
            source (NODE_T): The source node.
            dest (NODE_T): The destination node.

        Returns:
            float: The weight of the edge.

        Raises:
            NodeNotFoundError: If either node doesn't exist.
            EdgeNotFoundError: If the edge doesn't exist.
        """
        self._validate_nodes_exist(source, dest)
        if dest not in self._adjacency[source]:
            raise EdgeNotFoundError(f"No edge from {source} to {dest}")
        return self._adjacency[source][dest]


class UnweightedGraph(BaseGraph[NODE_T]):
    """A graph with unweighted edges stored as adjacency sets."""
    
    def __init__(self):
        super().__init__()
        self._adjacency: Dict[NODE_T, Set[NODE_T]] = defaultdict(set)

    def add_edge(self, source: NODE_T, dest: NODE_T) -> None:
        """Add an edge between two nodes.

        Args:
            source (NODE_T): The source node.
            dest (NODE_T): The destination node.
        """
        self.add_node(source)
        self.add_node(dest)
        self._adjacency[source].add(dest)

    def get_edges(self, source: NODE_T) -> Set[NODE_T]:
        """Get the edges connected to a given source node.

        Args:
            source (NODE_T): The source node.

        Returns:
            Set[NODE_T]: A set of nodes connected to the source.

        Raises:
            NodeNotFoundError: If the source node doesn't exist.
        """
        self._validate_nodes_exist(source)
        return self._adjacency[source].copy()
    
    def has_edge(self, source: NODE_T, dest: NODE_T) -> bool:
        """Check if an edge exists between two nodes.

        Args:
            source (NODE_T): The source node.
            dest (NODE_T): The destination node.

        Returns:
            bool: True if the edge exists, False otherwise.

        Raises:
            NodeNotFoundError: If either node doesn't exist.
        """
        self._validate_nodes_exist(source, dest)
        return dest in self._adjacency[source]


class MatchingGraph(Graph[NODE_T]):
    """A specialized graph for matching algorithms with residual graph support."""
    
    def __init__(self, source: NODE_T, sink: NODE_T):
        if source == sink:
            raise ValueError("Source and sink must be different nodes")
            
        self._adjacency = defaultdict(lambda: defaultdict(int))
        self._residual = defaultdict(lambda: defaultdict(int))
        self._nodes = set()
        self._source = source
        self._sink = sink
        # Add source and sink to nodes set
        self._nodes.add(source)
        self._nodes.add(sink)

    def reset_residual_graph(self) -> None:
        """Reset the residual graph to its initial state."""
        self._residual = defaultdict(lambda: defaultdict(int))

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

        Raises:
            TypeError: If weight is not an integer.
            ValueError: If weight is negative.
        """
        if not isinstance(w, int):
            raise TypeError("Edge weight must be an integer")
        if w < 0:
            raise ValueError("Edge weight cannot be negative")
            
        self._adjacency[u][v] = w
        self._nodes.add(v)
        self._nodes.add(u)

    def add_node(self, u: NODE_T) -> None:
        """Add a node to the graph.

        Args:
            u (NODE_T): The node to be added.

        Raises:
            ValueError: If trying to add source or sink nodes (they're managed automatically).
        """
        if u == self._source or u == self._sink:
            raise ValueError("Cannot manually add source or sink nodes")
        self._adjacency[u] = defaultdict(int)
        self._nodes.add(u)

    def get_edges(self, u: NODE_T) -> Dict[NODE_T, int]:
        """Get the edges connected to a given node.

        Args:
            u (NODE_T): The node.

        Returns:
            Dict[NODE_T, int]: A dictionary of edges connected to the node.

        Raises:
            NodeNotFoundError: If the node doesn't exist.
        """
        if u not in self._nodes:
            raise NodeNotFoundError(f"Node {u} not found in graph")
        return dict(self._adjacency[u])

    def get_residual_edges(self, u: NODE_T) -> Dict[NODE_T, int]:
        """Get the residual edges connected to a given node.

        Args:
            u (NODE_T): The node.

        Returns:
            Dict[NODE_T, int]: A dictionary of residual edges connected to the node.

        Raises:
            NodeNotFoundError: If the node doesn't exist.
        """
        if u not in self._nodes:
            raise NodeNotFoundError(f"Node {u} not found in graph")
        return dict(self._residual[u])

    def get_nodes(self) -> Iterator[NODE_T]:
        """Return an iterator over all nodes in the graph.

        Returns:
            Iterator[NODE_T]: An iterator over the nodes in the graph.
        """
        return iter(self._nodes)

    def get_idx(self, node: NODE_T) -> int:
        """Get the index of a node.

        Args:
            node (NODE_T): The node.

        Returns:
            int: The index of the node, or -1 if not found.

        Raises:
            NodeNotFoundError: If the node doesn't exist.
        """
        if node not in self._nodes:
            raise NodeNotFoundError(f"Node {node} not found in graph")
            
        idx = 0
        for n in self._nodes:
            if n == node:
                return idx
            idx += 1
        return -1  # Should never reach here

    def get_residual_nodes(self) -> Iterator[NODE_T]:
        """Return an iterator over the residual nodes.

        Returns:
            Iterator[NODE_T]: An iterator over the residual nodes.
        """
        return iter(self._residual.keys())

    def edge_exists(self, u: NODE_T, v: NODE_T) -> bool:
        """Check if an edge exists between two nodes.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.

        Returns:
            bool: True if the edge exists, False otherwise.

        Raises:
            NodeNotFoundError: If either node doesn't exist.
        """
        if u not in self._nodes or v not in self._nodes:
            raise NodeNotFoundError(f"Node {u} or {v} not found in graph")
        return self._adjacency[u][v] > 0

    def residual_edge_exists(self, u: NODE_T, v: NODE_T) -> bool:
        """Check if a residual edge exists between two nodes.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.

        Returns:
            bool: True if the residual edge exists, False otherwise.

        Raises:
            NodeNotFoundError: If either node doesn't exist.
        """
        if u not in self._nodes or v not in self._nodes:
            raise NodeNotFoundError(f"Node {u} or {v} not found in graph")
        return self._residual[u][v] > 0

    def get_edge_weight(self, u: NODE_T, v: NODE_T) -> float:
        """Get the weight of an edge between two nodes.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.

        Returns:
            float: The weight of the edge, or 0 if it does not exist.

        Raises:
            NodeNotFoundError: If either node doesn't exist.
        """
        if u not in self._nodes or v not in self._nodes:
            raise NodeNotFoundError(f"Node {u} or {v} not found in graph")
        return self._adjacency[u][v]

    def get_residual_edge_weight(self, u: NODE_T, v: NODE_T) -> float:
        """Get the weight of a residual edge between two nodes.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.

        Returns:
            float: The weight of the residual edge, or 0 if it does not exist.

        Raises:
            NodeNotFoundError: If either node doesn't exist.
        """
        if u not in self._nodes or v not in self._nodes:
            raise NodeNotFoundError(f"Node {u} or {v} not found in graph")
        return self._residual[u][v]

    def update_residual_edge_weight(self, u: NODE_T, v: NODE_T, w: float) -> None:
        """Update the weight of a residual edge.

        Args:
            u (NODE_T): The source node.
            v (NODE_T): The destination node.
            w (float): The new weight of the residual edge.

        Raises:
            NodeNotFoundError: If either node doesn't exist.
            ValueError: If weight is negative.
        """
        if u not in self._nodes or v not in self._nodes:
            raise NodeNotFoundError(f"Node {u} or {v} not found in graph")
        if w < 0:
            raise ValueError("Residual edge weight cannot be negative")
        self._residual[u][v] = w

    def preliminary_assignment(self, u: NODE_T, v: NODE_T, w: int = 1) -> None:
        """Make a preliminary assignment for a bipartite graph.

        Args:
            u (NODE_T): The first node.
            v (NODE_T): The second node.
            w (int, optional): The weight of the assignment. Defaults to 1.

        Raises:
            NodeNotFoundError: If either node doesn't exist.
            ValueError: If weight is not positive.
        """
        if u not in self._nodes or v not in self._nodes:
            raise NodeNotFoundError(f"Node {u} or {v} not found in graph")
        if w <= 0:
            raise ValueError("Assignment weight must be positive")
            
        # For bipartite graphs to add initial flow
        self._residual[self._source][u] += w
        self._residual[u][v] += w
        self._residual[v][self._sink] += w

    def visualize(self, fname: str = "test.png") -> None:
        """Visualize the graph and save it to a file.

        Args:
            fname (str, optional): The filename to save the visualization. Defaults to 'test.png'.
        """
        nx_graph = nx.DiGraph()

        # add nodes and edges to graph
        for u in self._adjacency:
            for v, w in self._adjacency[u].items():
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

        for u in self._adjacency:
            if u != self._source and u != self._sink:
                if any(v == self._sink for v in self._adjacency[u]):
                    layers["sink_layer"].append(u)
                elif any(v == self._source for v in self._adjacency[u]):
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
            if v in self._residual[u] and self._residual[u][v] > 0:
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
        return len(self._nodes)