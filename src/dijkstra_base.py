"""
Basic Dijkstra algorithm implementation using Priority Queue
"""
# src/dijkstra_base.py
import heapq
from typing import List, Dict, Tuple

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> List[int]:
    """
    Dijkstra's algorithm with priority queue optimization.
    
    Args:
        graph: Adjacency list representation of the graph. 
               Format: {node: [(neighbor1, weight1), (neighbor2, weight2), ...]}
        start: Starting node index.
    
    Returns:
        List of shortest distances from start node to all other nodes.
    """
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    visited = [False] * n
    heap = [(0, start)]  # (distance, node)
    
    while heap:
        current_dist, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        
        for v, weight in graph[u]:
            if dist[v] > current_dist + weight:
                dist[v] = current_dist + weight
                heapq.heappush(heap, (dist[v], v))
    
    return dist