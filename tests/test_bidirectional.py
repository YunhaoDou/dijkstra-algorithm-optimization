"""Tests for src/bidirectional.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.bidirectional import bidirectional_dijkstra
from src.dijkstra_base import dijkstra
from src.utils import grid_graph, random_graph


def test_matches_dijkstra_small():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    _, expected_d = dijkstra(graph, 0, 3)
    path, d = bidirectional_dijkstra(graph, 0, 3)
    assert d == expected_d
    assert path[0] == 0 and path[-1] == 3


def test_matches_dijkstra_grid():
    g = grid_graph(8, 8, seed=3)
    _, expected_d = dijkstra(g, (0, 0), (7, 7))
    _, d = bidirectional_dijkstra(g, (0, 0), (7, 7))
    assert d == expected_d


def test_matches_dijkstra_random_directed():
    g = random_graph(40, edge_prob=0.08, seed=11)
    for end in (5, 10, 30):
        if end in g:
            _, ed = dijkstra(g, 0, end)
            _, bd = bidirectional_dijkstra(g, 0, end)
            assert ed == bd, f"mismatch for end={end}: {ed} vs {bd}"


def test_unreachable():
    graph = {0: [(1, 1)], 1: [], 2: []}
    _, d = bidirectional_dijkstra(graph, 0, 2)
    assert d == math.inf


def test_start_equals_end():
    graph = {0: [(1, 1)], 1: []}
    path, d = bidirectional_dijkstra(graph, 0, 0)
    assert path == [0] and d == 0


if __name__ == "__main__":
    test_matches_dijkstra_small()
    test_matches_dijkstra_grid()
    test_matches_dijkstra_random_directed()
    test_unreachable()
    test_start_equals_end()
    print("test_bidirectional: OK")
