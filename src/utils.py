"""Graph utilities: type aliases, validation, reversal, generators."""
import random
from typing import Dict, Hashable, List, Tuple, Union

Number = Union[int, float]
Graph = Dict[Hashable, List[Tuple[Hashable, Number]]]


def validate_graph(graph: Graph) -> None:
    """Raise a descriptive error if `graph` is not a valid weighted adjacency list.

    Required shape:
        {node: [(neighbor, weight), ...], ...}
    where weight is a non-negative number (Dijkstra cannot handle negative weights).
    """
    if not isinstance(graph, dict):
        raise TypeError(f"graph must be a dict, got {type(graph).__name__}")
    for node, edges in graph.items():
        if not isinstance(edges, list):
            raise TypeError(f"graph[{node!r}] must be a list, got {type(edges).__name__}")
        for edge in edges:
            if not (isinstance(edge, tuple) and len(edge) == 2):
                raise TypeError(f"each edge in graph[{node!r}] must be a (neighbor, weight) tuple, got {edge!r}")
            _, weight = edge
            if not isinstance(weight, (int, float)):
                raise TypeError(f"weight in graph[{node!r}] must be numeric, got {weight!r}")
            if weight < 0:
                raise ValueError(f"weight in graph[{node!r}] must be non-negative for Dijkstra (got {weight})")


def reverse_graph(graph: Graph) -> Graph:
    """Build the reverse adjacency list (for bidirectional search on directed graphs)."""
    rev: Graph = {n: [] for n in graph}
    for u, edges in graph.items():
        for v, w in edges:
            rev.setdefault(v, []).append((u, w))
    return rev


def random_graph(n: int, edge_prob: float = 0.1, max_weight: int = 10, seed: int = 0) -> Graph:
    """Generate a random directed weighted graph with n nodes labelled 0..n-1."""
    rng = random.Random(seed)
    graph: Graph = {i: [] for i in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < edge_prob:
                graph[u].append((v, rng.randint(1, max_weight)))
    return graph


def grid_graph(width: int, height: int, max_weight: int = 5, seed: int = 0) -> Graph:
    """Generate a 4-connected grid graph with random weights. Nodes are (x, y) tuples."""
    rng = random.Random(seed)
    graph: Graph = {}
    for x in range(width):
        for y in range(height):
            edges = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    edges.append(((nx, ny), rng.randint(1, max_weight)))
            graph[(x, y)] = edges
    return graph
