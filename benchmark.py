"""Benchmark: 6 algorithms on grids. All single-pair tests agree on the optimal distance."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.a_star import a_star, manhattan_2d, zero_heuristic
from src.bellman_ford import bellman_ford
from src.bidirectional import bidirectional_dijkstra
from src.dijkstra_base import dijkstra
from src.floyd_warshall import floyd_warshall
from src.utils import grid_graph


def time_it(fn, *args, **kwargs):
    """Return (elapsed_ms, result)."""
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    return (time.perf_counter() - t0) * 1000, result


def main():
    print("=" * 78)
    print("Single-pair shortest path benchmark (start = (0,0), goal = (N-1, N-1))")
    print("=" * 78)
    sizes = [10, 30, 50, 80]
    print(
        f"{'N':>4} {'Dijkstra':>10} {'BF':>10} {'Bidir':>10} {'A* zero':>10} {'A* Manh':>10}"
    )
    print(f"{'':>4} {'(ms)':>10} {'(ms)':>10} {'(ms)':>10} {'(ms)':>10} {'(ms)':>10}")
    print("-" * 60)

    for n in sizes:
        graph = grid_graph(n, n, seed=0)
        start, goal = (0, 0), (n - 1, n - 1)

        t_dij, (_, d_dij) = time_it(dijkstra, graph, start, goal)
        t_bf,  (_, d_bf)  = time_it(bellman_ford, graph, start, goal)
        t_bi,  (_, d_bi)  = time_it(bidirectional_dijkstra, graph, start, goal)
        t_az,  (_, d_az)  = time_it(a_star, graph, start, goal, heuristic=zero_heuristic)
        t_am,  (_, d_am)  = time_it(a_star, graph, start, goal, heuristic=manhattan_2d)

        assert d_dij == d_bf == d_bi == d_az == d_am, (
            f"distances disagree at n={n}"
        )

        print(f"{n:>4} {t_dij:>10.2f} {t_bf:>10.2f} {t_bi:>10.2f} {t_az:>10.2f} {t_am:>10.2f}")

    print()
    print("=" * 78)
    print("All-pairs benchmark (Floyd-Warshall vs N x Dijkstra)")
    print("=" * 78)
    print(f"{'N':>4} {'Floyd (ms)':>14} {'N x Dijk (ms)':>16} {'Winner':>10}")
    print("-" * 50)
    for n in [10, 15, 20]:
        graph = grid_graph(n, n, seed=0)
        t_fw, _ = time_it(floyd_warshall, graph)
        t0 = time.perf_counter()
        for u in graph:
            dijkstra(graph, u)
        t_nd = (time.perf_counter() - t0) * 1000
        winner = "Floyd" if t_fw < t_nd else "N x Dijk"
        print(f"{n:>4} {t_fw:>14.2f} {t_nd:>16.2f} {winner:>10}")

    print()
    print("Takeaways:")
    print("  - Bellman-Ford is consistently slower than Dijkstra. Only use it if you")
    print("    need negative weights or cycle detection.")
    print("  - Floyd-Warshall (V^3) beats N x Dijkstra (V * (V+E) log V) on dense")
    print("    graphs but loses on sparse graphs as V grows.")
    print("  - A* with a good heuristic wins on large grids; on small ones the")
    print("    heuristic overhead can outweigh the savings.")


if __name__ == "__main__":
    main()
