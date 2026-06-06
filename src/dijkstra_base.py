"""Classic Dijkstra's algorithm with a binary heap.

Time complexity: O((V + E) log V).

This is the baseline. The other modules optimize this baseline along different axes:
  - `bidirectional`: search from both ends.
  - `a_star`: prune with an admissible heuristic.
  - `layered_graph`: handle state-augmented or time-expanded variants.
"""
import heapq
from typing import Dict, Hashable, List, Optional, Tuple, Union

from .utils import Graph, Number, validate_graph


def dijkstra(
    graph: Graph,
    start: Hashable,
    end: Optional[Hashable] = None,
) -> Union[Dict[Hashable, Number], Tuple[List[Hashable], Number]]:
    """Find shortest path(s) from `start` in a non-negative-weight graph.

    Args:
        graph: adjacency list as {node: [(neighbor, weight), ...]}
        start: source node, must exist in graph
        end: optional target. If given, the function returns a single (path, distance).
             If None, returns a dict of distances from start to every reachable node.

    Returns:
        If `end` is None: dict mapping each node to its shortest distance from `start`
            (unreachable nodes have distance float('inf')).
        If `end` is given: tuple (path_as_list, distance). If unreachable, ([], inf).

    Raises:
        TypeError / ValueError: on malformed graph.
        KeyError: if start or end is not in graph.
    """
    validate_graph(graph)
    if start not in graph:
        raise KeyError(f"start={start!r} not in graph")
    if end is not None and end not in graph:
        raise KeyError(f"end={end!r} not in graph")

    distances: Dict[Hashable, Number] = {n: float("inf") for n in graph}
    distances[start] = 0
    previous: Dict[Hashable, Optional[Hashable]] = {n: None for n in graph}
    pq: List[Tuple[Number, Hashable]] = [(0, start)]
    visited: set = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        if end is not None and u == end:
            break
        visited.add(u)

        for v, w in graph.get(u, []):
            if v in visited:
                continue
            alt = d + w
            if alt < distances.get(v, float("inf")):
                distances[v] = alt
                previous[v] = u
                heapq.heappush(pq, (alt, v))

    if end is None:
        return distances

    if distances[end] == float("inf"):
        return [], float("inf")

    # Reconstruct path by walking previous pointers
    path: List[Hashable] = []
    cur: Optional[Hashable] = end
    while cur is not None:
        path.append(cur)
        cur = previous[cur]
    path.reverse()
    return path, distances[end]
