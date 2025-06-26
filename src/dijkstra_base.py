"""
Dijkstra's Algorithm Implementation

This module provides an optimized implementation of Dijkstra's shortest path algorithm with:
- Priority queue optimization using heapq
- Path reconstruction with reverse tracking
- Comprehensive input validation
- Time complexity: O((V + E) log V) where V is vertices and E is edges

Example usage:
```python
# 定义图结构
graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: []
}

# 计算从起点到所有节点的最短路径
distances = dijkstra(graph, start=0)
print(distances)  # {0: 0, 1: 3, 2: 1, 3: 4}

# 查找两点间最短路径
path, distance = dijkstra(graph, start=0, end=3)
print(path)       # [0, 2, 1, 3]
print(distance)   # 4
```

For more details, see <mcurl name="Wikipedia" url="https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm"></mcurl>
"""
import heapq
from typing import Dict, Tuple, List, Optional, Union


def dijkstra(
    graph: Dict[int, List[Tuple[int, Union[int, float]]], 
    start: int, 
    end: Optional[int] = None
) -> Union[Dict[int, Union[int, float]], Tuple[List[int], Union[int, float]]:
    """
    Find shortest paths in a weighted graph using Dijkstra's algorithm.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        end: Optional target node for path reconstruction

    Returns:
        If end is None: Dictionary of shortest distances from start to all nodes
        If end is provided: Tuple of (path, distance)
    """
    # Validate graph structure
    if not isinstance(graph, dict):
        raise TypeError("Graph must be a dictionary")
    for node in graph:
        if not isinstance(node, int):
            raise TypeError(f"Node {node} must be an integer")
        if not isinstance(graph[node], list):
            raise TypeError(f"Edges for node {node} must be a list")
        for edge in graph[node]:
            if not isinstance(edge, tuple) or len(edge) != 2:
                raise TypeError(f"Invalid edge format in node {node}")
            neighbor, weight = edge
            if not isinstance(neighbor, int):
                raise TypeError(f"Neighbor must be integer in edge from {node}")
            if not isinstance(weight, (int, float)) or weight < 0:
                raise ValueError(f"Invalid weight {weight} in edge from {node} to {neighbor}")

    # Validate start and end nodes
    if start not in graph:
        raise ValueError(f"Start node {start} not found in graph")
    if end is not None and end not in graph:
        raise ValueError(f"End node {end} not found in graph")

    # Initialize algorithm data structures
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, start)]
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if end is not None and current_node == end:
            break

        if current_node in visited:
            continue
        visited.add(current_node)

        # Relaxation process
        for neighbor, weight in graph[current_node]:
            if neighbor in visited:
                continue

            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Path reconstruction
    if end is not None:
        if distances[end] == float('inf'):
            return [], float('inf')

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        return path, distances[end]

    return distances