"""Tests for src/layered_graph.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.layered_graph import layered_shortest_path


def test_at_most_k_shortcuts():
    """0 -> 1 -> 2 -> 3 -> 4 (each weight 1, total 4)
    plus 0 -> 4 shortcut (weight 100).
    Best is the direct path; shortcut shouldn't fool us."""
    direct = {0: [(1, 1)], 1: [(2, 1)], 2: [(3, 1)], 3: [(4, 1)], 4: []}
    shortcuts = {0: [(4, 100)]}
    K = 1

    def edges_fn(state):
        node, used = state
        for v, w in direct.get(node, []):
            yield (v, used), w
        if used < K:
            for v, w in shortcuts.get(node, []):
                yield (v, used + 1), w

    def is_goal(state):
        return state[0] == 4

    path, d = layered_shortest_path(edges_fn, (0, 0), is_goal)
    assert d == 4
    assert path[0] == (0, 0) and path[-1][0] == 4


def test_shortcut_actually_helps():
    """If direct path is very long, shortcut should win."""
    direct = {0: [(1, 50)], 1: [(2, 50)], 2: [(3, 50)], 3: [(4, 50)], 4: []}
    shortcuts = {0: [(4, 10)]}
    K = 1

    def edges_fn(state):
        node, used = state
        for v, w in direct.get(node, []):
            yield (v, used), w
        if used < K:
            for v, w in shortcuts.get(node, []):
                yield (v, used + 1), w

    def is_goal(state):
        return state[0] == 4

    _, d = layered_shortest_path(edges_fn, (0, 0), is_goal)
    assert d == 10


if __name__ == "__main__":
    test_at_most_k_shortcuts()
    test_shortcut_actually_helps()
    print("test_layered: OK")
