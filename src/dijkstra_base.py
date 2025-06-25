"""
Dijkstra's Algorithm Implementation with Priority Queue Optimization

This implementation follows the principles of The Zen of Python:
- Explicit is better than implicit
- Simple is better than complex
- Readability counts
"""

import heapq
from typing import List, Dict, Tuple


def dijkstra(
    graph: Dict[int, List[Tuple[int, int]]], 
    start: int
) -> List[int]:
    """
    Calculate shortest paths from start node using Dijkstra's algorithm.
    
    Args:
        graph: Adjacency list representation of the graph.
               Format: {node: [(neighbor, weight), ...]}
        start: Index of the starting node
        
    Returns:
        List where index represents node and value represents shortest distance
        from start node. Unreachable nodes have distance of infinity.
    """
    # Initialize data structures
    num_nodes = len(graph)
    distances = [float('inf')] * num_nodes
    distances[start] = 0
    
    visited_nodes = [False] * num_nodes
    priority_queue = [(0, start)]  # (distance, node)
    
    # Process nodes in order of increasing distance
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Skip already visited nodes
        if visited_nodes[current_node]:
            continue
            
        visited_nodes[current_node] = True
        
        # Update distances to neighbors
        for neighbor, weight in graph[current_node]:
            new_distance = current_distance + weight
            
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))
    
    return distances