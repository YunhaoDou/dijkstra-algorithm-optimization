"""Benchmark: plain Dijkstra vs Bidirectional vs A* (zero / Manhattan) on grids."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.a_star import a_star, manhattan_2d, zero_heuristic
from src.bidirectional import bidirectional_dijkstra
from src.dijkstra_base import dijkstra
from src.utils import grid_graph


def time_it(fn, *args, **kwargs):
    """Return (elapsed_ms, result)."""
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    return (time.perf_counter() - t0) * 1000, result


def main():
    sizes = [10, 30, 50, 80]
    print(f"{'Size NxN':>10} {'Dijkstra':>12} {'Bidir':>10} {'A* zero':>10} {'A* Manhattan':>14}")
    print(f"{'(nodes)':>10} {'(ms)':>12} {'(ms)':>10} {'(ms)':>10} {'(ms)':>14}")
    print("-" * 60)

    for n in sizes:
        graph = grid_graph(n, n, seed=0)
        start, goal = (0, 0), (n - 1, n - 1)

        t_dij, (_, d_dij) = time_it(dijkstra, graph, start, goal)
        t_bi,  (_, d_bi)  = time_it(bidirectional_dijkstra, graph, start, goal)
        t_az,  (_, d_az)  = time_it(a_star, graph, start, goal, heuristic=zero_heuristic)
        t_am,  (_, d_am)  = time_it(a_star, graph, start, goal, heuristic=manhattan_2d)

        # Correctness: all four must agree on the optimal distance.
        assert d_dij == d_bi == d_az == d_am, (
            f"distances disagree at n={n}: dij={d_dij}, bi={d_bi}, az={d_az}, am={d_am}"
        )

        print(f"{n:>10} {t_dij:>12.2f} {t_bi:>10.2f} {t_az:>10.2f} {t_am:>14.2f}")

    print()
    print("All algorithms produced identical distances. The differences above are")
    print("only in how much of the graph each algorithm needed to explore.")


if __name__ == "__main__":
    main()
