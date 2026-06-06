"""Visualize the exploration footprint of Dijkstra vs A* on a grid.

This example shows the *real* reason A* is faster: it explores far fewer nodes
when the heuristic guides it toward the goal.

Saves a PNG to ./visualization.png.
Requires: matplotlib (pip install matplotlib).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("This example needs matplotlib. Install with: pip install matplotlib")
    sys.exit(1)

import heapq
from src.a_star import manhattan_2d
from src.utils import grid_graph

WIDTH, HEIGHT = 30, 20
START, GOAL = (0, 0), (29, 19)
graph = grid_graph(WIDTH, HEIGHT, max_weight=3, seed=7)


def dijkstra_explored(graph, start, goal):
    """Run Dijkstra and return the set of nodes that were closed (explored)."""
    dist = {start: 0}
    pq = [(0, start)]
    closed = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in closed:
            continue
        closed.add(u)
        if u == goal:
            break
        for v, w in graph.get(u, []):
            alt = d + w
            if alt < dist.get(v, float("inf")):
                dist[v] = alt
                heapq.heappush(pq, (alt, v))
    return closed


def a_star_explored(graph, start, goal):
    dist = {start: 0}
    pq = [(manhattan_2d(start, goal), start)]
    closed = set()
    while pq:
        _, u = heapq.heappop(pq)
        if u in closed:
            continue
        closed.add(u)
        if u == goal:
            break
        for v, w in graph.get(u, []):
            alt = dist[u] + w
            if alt < dist.get(v, float("inf")):
                dist[v] = alt
                heapq.heappush(pq, (alt + manhattan_2d(v, goal), v))
    return closed


dij_explored = dijkstra_explored(graph, START, GOAL)
a_star_explored_set = a_star_explored(graph, START, GOAL)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for ax, explored, title in [
    (axes[0], dij_explored, f"Dijkstra: explored {len(dij_explored)} nodes"),
    (axes[1], a_star_explored_set, f"A* (Manhattan): explored {len(a_star_explored_set)} nodes"),
]:
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = "#239a3b" if (x, y) in explored else "#ecf0f1"
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color, ec="white"))
    ax.add_patch(plt.Rectangle(START, 1, 1, color="#3498db", ec="white"))
    ax.add_patch(plt.Rectangle(GOAL, 1, 1, color="#e74c3c", ec="white"))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])

plt.suptitle(
    f"Exploration footprint on {WIDTH}x{HEIGHT} grid (green = explored, blue = start, red = goal)",
    y=1.02,
)
plt.tight_layout()
plt.savefig("visualization.png", dpi=120, bbox_inches="tight")
print(f"Dijkstra explored: {len(dij_explored)} nodes")
print(f"A* explored:        {len(a_star_explored_set)} nodes")
print(f"A* reduction:       {(1 - len(a_star_explored_set) / len(dij_explored)) * 100:.1f}%")
print("Saved to visualization.png")
