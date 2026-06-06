"""Layered graph: cheapest flight with at most K stops."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.layered_graph import layered_shortest_path

# Toy flight network. Edges: source -> [(dest, price)]
flights = {
    "BJ": [("SH", 1500), ("GZ", 1800), ("HK", 3200)],
    "SH": [("HK", 1200), ("GZ", 900)],
    "GZ": [("HK", 600)],
    "HK": [],
}

MAX_STOPS = 1  # at most 1 stop = at most 2 flight segments


def edges(state):
    """A state is (current_city, segments_used). We can take another segment
    only if we haven't exceeded MAX_STOPS + 1 segments."""
    city, segments = state
    if segments >= MAX_STOPS + 1:
        return
    for dest, price in flights.get(city, []):
        yield (dest, segments + 1), price


def is_goal(state):
    return state[0] == "HK"


path, cost = layered_shortest_path(edges, ("BJ", 0), is_goal)
print(f"Cheapest BJ -> HK with at most {MAX_STOPS} stop(s):")
for city, segs in path:
    print(f"  {city} (after {segs} segment(s))")
print(f"Total cost: {cost}")
