# Dijkstra Algorithm Optimization Toolkit

Six runnable shortest-path algorithms behind a unified API, with a head-to-head benchmark.

**Language**: [简体中文](./README.md) · **English**

![Tests](https://github.com/YunhaoDou/dijkstra-algorithm-optimization/actions/workflows/test.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

## What's inside

| Algorithm | File | Complexity | Use when |
|-----------|------|------------|----------|
| Dijkstra | `src/dijkstra_base.py` | O((V+E) log V) | Single-source, non-negative weights, sparse graphs |
| Bidirectional Dijkstra | `src/bidirectional.py` | Same worst case, smaller constants in practice | Single-pair, long paths |
| A* | `src/a_star.py` | Same worst case, huge speedup with a good heuristic | When an admissible heuristic exists (e.g. grid maps) |
| Bellman-Ford | `src/bellman_ford.py` | O(V * E) | Negative weights; detect negative cycles |
| Floyd-Warshall | `src/floyd_warshall.py` | O(V^3) | All-pairs distances on small/dense graphs |
| Layered shortest path | `src/layered_graph.py` | O((V*L)(E*L) log(V*L)) | Stateful constraints: "at most K transfers", time-dependent edges |

All six produce identical distances when given the same input. They differ in how many nodes they expand.

## Install

```bash
git clone https://github.com/YunhaoDou/dijkstra-algorithm-optimization
cd dijkstra-algorithm-optimization
```

No third-party dependencies for the core. Python 3.10+ stdlib is enough.

Optional:
```bash
pip install matplotlib  # for examples/visualize.py
pip install pytest      # for `pytest tests/` instead of running each test file
```

Or as a package:
```bash
pip install -e .
```

## Quick start

```python
from src.dijkstra_base import dijkstra

graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("D", 1)],
    "C": [("B", 2), ("D", 5)],
    "D": [],
}

# All distances from A
distances = dijkstra(graph, start="A")
# {'A': 0, 'B': 3, 'C': 1, 'D': 4}

# Single source-to-target (path reconstruction included)
path, dist = dijkstra(graph, start="A", end="D")
# path=['A', 'C', 'B', 'D'], dist=4
```

Nodes can be any hashable type (int, str, tuple).

## Tests

```bash
# No pytest needed
for f in tests/test_*.py; do python "$f"; done

# Or with pytest if installed
python -m pytest tests/
```

Expected:
```
test_a_star: OK
test_bellman_ford: OK
test_bidirectional: OK
test_dijkstra: OK
test_floyd_warshall: OK
test_layered: OK
```

CI runs the full suite on Python 3.10, 3.11, 3.12 every push.

## Run examples

```bash
python examples/basic_usage.py       # tiny graph, all distances + one path
python examples/road_network.py      # A* on a 20x20 grid
python examples/time_expanded.py     # layered: cheapest flight with at most K stops
python examples/visualize.py         # plot Dijkstra vs A* exploration footprint
```

`visualize.py` writes `visualization.png` showing how many nodes each algorithm expanded — A* should be dramatically smaller when start and goal are far apart.

## Benchmark

```bash
python benchmark.py
```

Sample output:

```
==============================================================================
Single-pair shortest path benchmark (start = (0,0), goal = (N-1, N-1))
==============================================================================
   N   Dijkstra         BF      Bidir    A* zero    A* Manh
           (ms)       (ms)       (ms)       (ms)       (ms)
------------------------------------------------------------
  10       0.17       0.23       0.17       0.16       0.16
  30       1.50       4.40       1.75       1.50       1.69
  50       4.22      16.51       5.25       4.41       4.89
  80      11.35      47.94      14.43      13.23      12.99
```

### Counterintuitive observation

On small uniform-weight grids, plain Dijkstra is roughly as fast as A* and bidirectional. The heuristic and reverse-graph overhead don't pay off until graphs get bigger or path lengths grow.

**When does optimization actually pay off?**

- Bidirectional Dijkstra: large graphs, long paths.
- A*: an informative admissible heuristic (e.g. straight-line distance on a map), goal far from start.
- Layered graph: **not for speed** — to express constraints (state, time) that plain Dijkstra cannot.
- Bellman-Ford: only if you need negative weights or cycle detection. It's strictly slower than Dijkstra otherwise.
- Floyd-Warshall: wins on dense graphs that fit V^3 budget; loses to N * Dijkstra on sparse graphs.

The core message: **pick algorithms by the structure of your problem, not by which one sounds fancier.**

## Layered shortest path in one snippet

Problems that look "beyond Dijkstra" are usually just Dijkstra on a state-augmented graph.

Example: **"Cheapest BJ -> HK with at most 1 stop"** — state is `(current_city, segments_used)`.

```python
def edges(state):
    city, segments = state
    if segments >= MAX_STOPS + 1:
        return
    for dest, price in flights[city]:
        yield (dest, segments + 1), price

path, cost = layered_shortest_path(edges, ("BJ", 0), lambda s: s[0] == "HK")
```

Full example: `examples/time_expanded.py`.

## Layout

```
dijkstra-algorithm-optimization/
├── README.md / README.en.md
├── LICENSE / pyproject.toml / requirements.txt
├── benchmark.py
├── .github/workflows/test.yml
├── src/
│   ├── dijkstra_base.py
│   ├── bidirectional.py
│   ├── a_star.py
│   ├── bellman_ford.py
│   ├── floyd_warshall.py
│   ├── layered_graph.py
│   └── utils.py
├── examples/
│   ├── basic_usage.py
│   ├── road_network.py
│   ├── time_expanded.py
│   └── visualize.py
└── tests/
    ├── test_dijkstra.py
    ├── test_bidirectional.py
    ├── test_a_star.py
    ├── test_bellman_ford.py
    ├── test_floyd_warshall.py
    └── test_layered.py
```

## License

[MIT](LICENSE)
