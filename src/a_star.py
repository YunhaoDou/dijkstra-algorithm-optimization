"""A* algorithm — Dijkstra with an admissible heuristic.

When the heuristic h(n, goal) never overestimates the true remaining cost,
A* returns the optimal path. When h is also consistent, no node is re-expanded.

This module decouples the heuristic from the algorithm so the same `a_star`
function works on any graph; pass a heuristic that fits your problem.
"""
import heapq
from typing import Callable, Dict, Hashable, List, Optional, Tuple

from .utils import Graph, Number, validate_graph

Heuristic = Callable[[Hashable, Hashable], Number]


def zero_heuristic(a: Hashable, b: Hashable) -> Number:
    """Trivial heuristic. A* with this is identical to plain Dijkstra."""
    return 0


def manhattan_2d(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Manhattan (L1) distance. Use for 4-connected grid graphs where nodes are (x, y)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_2d(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """Euclidean (L2) distance. Admissible on grids that allow diagonal moves."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def a_star(
    graph: Graph,
    start: Hashable,
    goal: Hashable,
    heuristic: Heuristic = zero_heuristic,
) -> Tuple[List[Hashable], Number]:
    """Shortest path from `start` to `goal` using A*.

    Args:
        graph: weighted adjacency list (see utils.Graph).
        start: source node.
        goal: target node.
        heuristic: function (node, goal) -> estimated remaining cost. Must be admissible.

    Returns:
        (path, distance), or ([], inf) if no path exists.
    """
    validate_graph(graph)
    if start not in graph:
        raise KeyError(f"start={start!r} not in graph")
    if goal not in graph:
        raise KeyError(f"goal={goal!r} not in graph")

    g_score: Dict[Hashable, Number] = {start: 0}
    came_from: Dict[Hashable, Optional[Hashable]] = {start: None}
    open_heap: List[Tuple[Number, Hashable]] = [(heuristic(start, goal), start)]
    closed: set = set()

    while open_heap:
        _, u = heapq.heappop(open_heap)
        if u in closed:
            continue
        if u == goal:
            path: List[Hashable] = []
            cur: Optional[Hashable] = u
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
            return path, g_score[u]
        closed.add(u)

        for v, w in graph.get(u, []):
            tentative = g_score[u] + w
            if tentative < g_score.get(v, float("inf")):
                g_score[v] = tentative
                came_from[v] = u
                heapq.heappush(open_heap, (tentative + heuristic(v, goal), v))

    return [], float("inf")
