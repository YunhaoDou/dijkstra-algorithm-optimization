"""A* on a 20x20 grid simulating a road network."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.a_star import a_star, manhattan_2d
from src.utils import grid_graph

g = grid_graph(20, 20, max_weight=3, seed=42)
start, goal = (0, 0), (19, 19)
path, distance = a_star(g, start, goal, heuristic=manhattan_2d)

print(f"From {start} to {goal}")
print(f"  path length: {len(path)} nodes")
print(f"  total cost:  {distance}")
print(f"  first 5:     {path[:5]}")
print(f"  last 5:      {path[-5:]}")
