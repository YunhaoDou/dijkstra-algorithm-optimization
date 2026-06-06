"""Bellman-Ford algorithm for single-source shortest path with negative edge weights.

Unlike Dijkstra, Bellman-Ford works correctly with negative weights and can
detect negative-weight cycles reachable from the source.

Time complexity: O(V * E). Slower than Dijkstra, but more general.

Use when:
  - You have negative edge weights (Dijkstra fails)
  - You need to detect negative cycles
  - You're doing currency arbitrage detection (a classic Bellman-Ford application)
"""
from typing import Dict, Hashable, List, Optional, Tuple, Union

from .utils import Graph, Number


class NegativeCycleError(ValueError):
    """Raised when a negative-weight cycle is reachable from the source."""


def bellman_ford(
    graph: Graph,
    start: Hashable,
    end: Optional[Hashable] = None,
) -> Union[Dict[Hashable, Number], Tuple[List[Hashable], Number]]:
    """Find shortest paths from `start`, allowing negative edge weights.

    Args:
        graph: adjacency list, may contain negative weights.
        start: source node.
        end: optional target. If given, returns (path, distance); else returns distances dict.

    Returns:
        Same shape as `dijkstra()`.

    Raises:
        NegativeCycleError: if a negative-weight cycle is reachable from `start`.
        KeyError: if start (or end) is not in graph.
    """
    if not isinstance(graph, dict):
        raise TypeError("graph must be a dict")
    if start not in graph:
        raise KeyError(f"start={start!r} not in graph")
    if end is not None and end not in graph:
        raise KeyError(f"end={end!r} not in graph")

    distances: Dict[Hashable, Number] = {n: float("inf") for n in graph}
    distances[start] = 0
    previous: Dict[Hashable, Optional[Hashable]] = {n: None for n in graph}

    n_nodes = len(graph)
    # Relax all edges V-1 times.
    for _ in range(n_nodes - 1):
        updated = False
        for u in graph:
            if distances[u] == float("inf"):
                continue
            for v, w in graph[u]:
                alt = distances[u] + w
                if alt < distances.get(v, float("inf")):
                    distances[v] = alt
                    previous[v] = u
                    updated = True
        if not updated:
            break  # early exit when no relaxation happens

    # One more pass to detect negative cycles.
    for u in graph:
        if distances[u] == float("inf"):
            continue
        for v, w in graph[u]:
            if distances[u] + w < distances.get(v, float("inf")):
                raise NegativeCycleError(
                    f"negative-weight cycle reachable through edge ({u}, {v}, w={w})"
                )

    if end is None:
        return distances

    if distances[end] == float("inf"):
        return [], float("inf")

    path: List[Hashable] = []
    cur: Optional[Hashable] = end
    while cur is not None:
        path.append(cur)
        cur = previous[cur]
    path.reverse()
    return path, distances[end]
