"""
A* Algorithm implementation
"""
# src/a_star.py
import heapq

def heuristic(node: int, goal: int) -> int:
    """
    Simple heuristic function (Manhattan distance as an example).
    Replace this with domain-specific heuristic.
    
    Args:
        node: Current node.
        goal: Target node.
    
    Returns:
        Heuristic estimate of distance from node to goal.
    """
    # Example: Manhattan distance on a grid (x, y coordinates)
    x1, y1 = node // 10, node % 10  # Assume nodes are on a 10x10 grid
    x2, y2 = goal // 10, goal % 10
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(graph: Dict[int, List[Tuple[int, int]]], start: int, goal: int) -> int:
    """
    A* algorithm for shortest path from start to goal.
    
    Args:
        graph: Adjacency list of the graph.
        start: Starting node.
        goal: Target node.
    
    Returns:
        Shortest path distance from start to goal.
    """
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0 + heuristic(start, goal), 0, start)]  # (f_score, g_score, node)
    
    while heap:
        f_score, g_score, u = heapq.heappop(heap)
        
        if u == goal:
            return g_score
        
        if g_score > dist[u]:
            continue
        
        for v, weight in graph[u]:
            tentative_g = g_score + weight
            if tentative_g < dist[v]:
                dist[v] = tentative_g
                f_score = tentative_g + heuristic(v, goal)
                heapq.heappush(heap, (f_score, tentative_g, v))
    
    return float('inf')  # No path found