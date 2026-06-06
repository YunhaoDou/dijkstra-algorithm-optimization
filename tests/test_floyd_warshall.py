"""Tests for src/floyd_warshall.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.dijkstra_base import dijkstra
from src.floyd_warshall import floyd_warshall, reconstruct_path


def test_distances_match_dijkstra():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    dist, _ = floyd_warshall(graph)
    for u in graph:
        for v, expected in dijkstra(graph, u).items():
            assert dist[u][v] == expected, f"mismatch at ({u},{v}): {dist[u][v]} vs {expected}"


def test_self_distance_zero():
    graph = {0: [(1, 5)], 1: []}
    dist, _ = floyd_warshall(graph)
    assert dist[0][0] == 0 and dist[1][1] == 0


def test_unreachable_is_inf():
    graph = {0: [(1, 1)], 1: [], 2: []}
    dist, _ = floyd_warshall(graph)
    assert dist[0][2] == math.inf


def test_path_reconstruction():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    _, next_node = floyd_warshall(graph)
    path = reconstruct_path(next_node, 0, 3)
    assert path == [0, 2, 1, 3]


def test_negative_weights_supported():
    graph = {0: [(1, 4), (2, 2)], 1: [(2, -3)], 2: [(3, 2)], 3: []}
    dist, _ = floyd_warshall(graph)
    assert dist[0][2] == 1
    assert dist[0][3] == 3


if __name__ == "__main__":
    test_distances_match_dijkstra()
    test_self_distance_zero()
    test_unreachable_is_inf()
    test_path_reconstruction()
    test_negative_weights_supported()
    print("test_floyd_warshall: OK")
