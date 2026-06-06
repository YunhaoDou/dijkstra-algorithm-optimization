"""Layered (state-expanded / time-expanded) shortest path.

When the graph carries additional state — number of transfers used so far,
current time of day, whether a "free shortcut" is still available — you can
solve it by Dijkstra on the product graph (node × state). To avoid building
the product graph explicitly (which can be huge), this module accepts a
*lazy edge function* that emits outgoing edges from a state on demand.

This is how you handle problems like:
  - "shortest path with at most K transfers"
  - "shortest path with time-dependent edge weights"
  - "shortest path where you can take 1 free shortcut"
  - "cheapest itinerary with a layover constraint"
"""
import heapq
from typing import Callable, Dict, Hashable, Iterable, List, Optional, Tuple

from .utils import Number

State = Tuple[Hashable, int]  # convention: (node, layer)
EdgesFn = Callable[[State], Iterable[Tuple[State, Number]]]
GoalFn = Callable[[State], bool]


def layered_shortest_path(
    edges_fn: EdgesFn,
    start: State,
    is_goal: GoalFn,
) -> Tuple[List[State], Number]:
    """Dijkstra on an implicit layered graph.

    Args:
        edges_fn: given a state, yield (next_state, weight) pairs. The graph
            is expanded lazily — you decide which transitions are valid.
        start: initial state.
        is_goal: predicate returning True when a state is a goal.

    Returns:
        (path_as_list_of_states, distance), or ([], inf) if no goal is reachable.
    """
    dist: Dict[State, Number] = {start: 0}
    came: Dict[State, Optional[State]] = {start: None}
    pq: List[Tuple[Number, State]] = [(0, start)]
    closed: set = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in closed:
            continue
        if is_goal(u):
            path: List[State] = []
            cur: Optional[State] = u
            while cur is not None:
                path.append(cur)
                cur = came[cur]
            path.reverse()
            return path, d
        closed.add(u)

        for v, w in edges_fn(u):
            alt = d + w
            if alt < dist.get(v, float("inf")):
                dist[v] = alt
                came[v] = u
                heapq.heappush(pq, (alt, v))

    return [], float("inf")
