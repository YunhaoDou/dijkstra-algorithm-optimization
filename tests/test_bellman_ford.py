"""Tests for src/bellman_ford.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.bellman_ford import NegativeCycleError, bellman_ford
from src.dijkstra_base import dijkstra


def test_matches_dijkstra_on_nonnegative():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    d_dij = dijkstra(graph, 0)
    d_bf = bellman_ford(graph, 0)
    assert d_dij == d_bf


def test_negative_weights_supported():
    # A negative edge that Dijkstra would mishandle but BF gets right.
    graph = {0: [(1, 4), (2, 2)], 1: [(2, -3)], 2: [(3, 2)], 3: []}
    distances = bellman_ford(graph, 0)
    assert distances == {0: 0, 1: 4, 2: 1, 3: 3}


def test_negative_cycle_detected():
    graph = {0: [(1, 1)], 1: [(2, -3)], 2: [(0, 1)]}
    try:
        bellman_ford(graph, 0)
    except NegativeCycleError:
        return
    raise AssertionError("expected NegativeCycleError for negative cycle")


def test_path_reconstruction():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    path, d = bellman_ford(graph, 0, 3)
    assert path == [0, 2, 1, 3] and d == 4


def test_unreachable():
    graph = {0: [(1, 1)], 1: [], 2: []}
    path, d = bellman_ford(graph, 0, 2)
    assert path == [] and d == math.inf


if __name__ == "__main__":
    test_matches_dijkstra_on_nonnegative()
    test_negative_weights_supported()
    test_negative_cycle_detected()
    test_path_reconstruction()
    test_unreachable()
    print("test_bellman_ford: OK")
