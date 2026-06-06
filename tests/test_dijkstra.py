"""Tests for src/dijkstra_base.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.dijkstra_base import dijkstra


def test_simple_graph_all_distances():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    distances = dijkstra(graph, start=0)
    assert distances == {0: 0, 1: 3, 2: 1, 3: 4}


def test_path_reconstruction():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    path, d = dijkstra(graph, start=0, end=3)
    assert path == [0, 2, 1, 3]
    assert d == 4


def test_unreachable():
    graph = {0: [(1, 1)], 1: [], 2: []}
    path, d = dijkstra(graph, start=0, end=2)
    assert path == [] and d == math.inf


def test_negative_weight_rejected():
    graph = {0: [(1, -1)], 1: []}
    try:
        dijkstra(graph, start=0)
    except ValueError:
        return
    raise AssertionError("expected ValueError for negative weight")


def test_string_node_labels():
    graph = {"A": [("B", 2)], "B": [("C", 3)], "C": []}
    path, d = dijkstra(graph, "A", "C")
    assert path == ["A", "B", "C"] and d == 5


if __name__ == "__main__":
    test_simple_graph_all_distances()
    test_path_reconstruction()
    test_unreachable()
    test_negative_weight_rejected()
    test_string_node_labels()
    print("test_dijkstra: OK")
