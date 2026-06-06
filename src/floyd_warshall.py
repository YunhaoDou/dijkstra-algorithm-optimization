"""Floyd-Warshall algorithm for all-pairs shortest paths.

Computes shortest paths between every pair of nodes in O(V^3) time.
Works with negative edge weights, fails on negative cycles (returns NaN/inf).

Use when:
  - You need ALL pairs of distances (not just from one source)
  - The graph is dense or small enough that V^3 is acceptable
  - You want a one-liner reference implementation
"""
from typing import Dict, Hashable, Tuple

from .utils import Graph, Number


def floyd_warshall(
    graph: Graph,
) -> Tuple[Dict[Hashable, Dict[Hashable, Number]], Dict[Tuple[Hashable, Hashable], Hashable]]:
    """Compute shortest distance between every pair of nodes.

    Args:
        graph: weighted adjacency list. May contain negative weights, but no negative cycles.

    Returns:
        (dist, next_node) where:
          dist[u][v] = shortest distance from u to v (inf if unreachable)
          next_node[(u, v)] = the next node on the shortest path from u to v
                              (use to reconstruct paths via reconstruct_path)
    """
    nodes = list(graph)
    dist: Dict[Hashable, Dict[Hashable, Number]] = {
        u: {v: float("inf") for v in nodes} for u in nodes
    }
    next_node: Dict[Tuple[Hashable, Hashable], Hashable] = {}

    for u in nodes:
        dist[u][u] = 0
        for v, w in graph.get(u, []):
            if w < dist[u][v]:
                dist[u][v] = w
                next_node[(u, v)] = v

    # Dynamic programming: for each intermediate node k, see if u->k->v is shorter than u->v.
    for k in nodes:
        for u in nodes:
            duk = dist[u][k]
            if duk == float("inf"):
                continue
            for v in nodes:
                alt = duk + dist[k][v]
                if alt < dist[u][v]:
                    dist[u][v] = alt
                    next_node[(u, v)] = next_node[(u, k)]

    return dist, next_node


def reconstruct_path(
    next_node: Dict[Tuple[Hashable, Hashable], Hashable],
    u: Hashable,
    v: Hashable,
) -> list:
    """Walk the next-node table to recover the actual path from u to v."""
    if (u, v) not in next_node and u != v:
        return []
    path = [u]
    cur = u
    while cur != v:
        cur = next_node[(cur, v)]
        path.append(cur)
    return path
