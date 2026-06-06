"""Bidirectional Dijkstra for single-pair shortest path.

Expands a search ball from both `start` and `end` simultaneously. The two balls
meet roughly in the middle, so the expanded volume is ~2 * (radius/2)^d versus
1 * radius^d for plain Dijkstra — a constant-factor speedup that becomes large
on long paths in dense graphs.

Termination criterion: when the sum of the top of both heaps exceeds the best
candidate distance found so far, no shorter path can exist.
"""
import heapq
from typing import Dict, Hashable, List, Optional, Tuple

from .utils import Graph, Number, reverse_graph, validate_graph


def bidirectional_dijkstra(
    graph: Graph,
    start: Hashable,
    end: Hashable,
) -> Tuple[List[Hashable], Number]:
    """Find the shortest path from start to end. Returns (path, distance) or ([], inf)."""
    validate_graph(graph)
    if start not in graph:
        raise KeyError(f"start={start!r} not in graph")
    if end not in graph:
        raise KeyError(f"end={end!r} not in graph")
    if start == end:
        return [start], 0

    # For directed-graph correctness, the backward search uses the reversed adjacency.
    backward_graph = reverse_graph(graph)

    # Forward state
    df: Dict[Hashable, Number] = {start: 0}
    pf: Dict[Hashable, Optional[Hashable]] = {start: None}
    hf: List[Tuple[Number, Hashable]] = [(0, start)]
    closed_f: set = set()

    # Backward state
    db: Dict[Hashable, Number] = {end: 0}
    pb: Dict[Hashable, Optional[Hashable]] = {end: None}
    hb: List[Tuple[Number, Hashable]] = [(0, end)]
    closed_b: set = set()

    best: Number = float("inf")
    meeting: Optional[Hashable] = None

    while hf and hb:
        # Standard termination: when top-of-both >= current best, done.
        if hf[0][0] + hb[0][0] >= best:
            break

        # Forward expansion
        d, u = heapq.heappop(hf)
        if u not in closed_f:
            closed_f.add(u)
            for v, w in graph.get(u, []):
                alt = d + w
                if alt < df.get(v, float("inf")):
                    df[v] = alt
                    pf[v] = u
                    heapq.heappush(hf, (alt, v))
                    if v in db:
                        cand = alt + db[v]
                        if cand < best:
                            best = cand
                            meeting = v

        if not hb:
            break

        # Backward expansion
        d, u = heapq.heappop(hb)
        if u in closed_b:
            continue
        closed_b.add(u)
        for v, w in backward_graph.get(u, []):
            alt = d + w
            if alt < db.get(v, float("inf")):
                db[v] = alt
                pb[v] = u
                heapq.heappush(hb, (alt, v))
                if v in df:
                    cand = alt + df[v]
                    if cand < best:
                        best = cand
                        meeting = v

    if meeting is None:
        return [], float("inf")

    # Reconstruct: walk pf from meeting back to start, then walk pb from meeting forward to end.
    left: List[Hashable] = []
    cur: Optional[Hashable] = meeting
    while cur is not None:
        left.append(cur)
        cur = pf.get(cur)
    left.reverse()

    right: List[Hashable] = []
    cur = pb.get(meeting)
    while cur is not None:
        right.append(cur)
        cur = pb.get(cur)

    return left + right, best
