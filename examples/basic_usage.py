"""Basic usage: shortest path on a tiny labelled graph."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.dijkstra_base import dijkstra

graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("D", 1)],
    "C": [("B", 2), ("D", 5)],
    "D": [],
}

print("All distances from A:", dijkstra(graph, start="A"))

path, distance = dijkstra(graph, start="A", end="D")
print(f"Shortest A -> D: {' -> '.join(path)}  (cost {distance})")
