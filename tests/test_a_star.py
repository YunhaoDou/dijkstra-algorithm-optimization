"""Tests for src/a_star.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.a_star import a_star, euclidean_2d, manhattan_2d, zero_heuristic
from src.dijkstra_base import dijkstra
from src.utils import grid_graph


def test_zero_heuristic_matches_dijkstra():
    g = grid_graph(6, 6, seed=1)
    _, a_d = a_star(g, (0, 0), (5, 5), heuristic=zero_heuristic)
    _, d_d = dijkstra(g, (0, 0), (5, 5))
    assert a_d == d_d


def test_manhattan_matches_dijkstra():
    g = grid_graph(6, 6, seed=2)
    _, a_d = a_star(g, (0, 0), (5, 5), heuristic=manhattan_2d)
    _, d_d = dijkstra(g, (0, 0), (5, 5))
    assert a_d == d_d


def test_euclidean_matches_dijkstra():
    g = grid_graph(6, 6, seed=3)
    _, a_d = a_star(g, (0, 0), (5, 5), heuristic=euclidean_2d)
    _, d_d = dijkstra(g, (0, 0), (5, 5))
    assert a_d == d_d


def test_unreachable():
    graph = {0: [(1, 1)], 1: [], 2: []}
    _, d = a_star(graph, 0, 2)
    assert d == math.inf


if __name__ == "__main__":
    test_zero_heuristic_matches_dijkstra()
    test_manhattan_matches_dijkstra()
    test_euclidean_matches_dijkstra()
    test_unreachable()
    print("test_a_star: OK")
