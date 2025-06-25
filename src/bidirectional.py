"""
Bidirectional Dijkstra algorithm implementation
"""
# src/bidirectional.py
import heapq

def bidirectional_dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int, end: int) -> int:
    """
    Bidirectional Dijkstra algorithm for shortest path from start to end.
    
    Args:
        graph: Adjacency list of the graph.
        start: Starting node.
        end: Target node.
    
    Returns:
        Shortest path distance from start to end.
    """
    n = len(graph)
    
    # Forward search from start
    dist_forward = [float('inf')] * n
    dist_forward[start] = 0
    heap_forward = [(0, start)]
    visited_forward = set()
    
    # Backward search from end
    dist_backward = [float('inf')] * n
    dist_backward[end] = 0
    heap_backward = [(0, end)]
    visited_backward = set()
    
    shortest_path = float('inf')
    
    while heap_forward and heap_backward:
        # Process forward search
        current_dist_f, u_f = heapq.heappop(heap_forward)
        if u_f in visited_forward:
            continue
        visited_forward.add(u_f)
        
        # Check if current node has been visited by backward search
        if u_f in visited_backward:
            shortest_path = min(shortest_path, current_dist_f + dist_backward[u_f])
        
        for v_f, weight_f in graph[u_f]:
            if dist_forward[v_f] > current_dist_f + weight_f:
                dist_forward[v_f] = current_dist_f + weight_f
                heapq.heappush(heap_forward, (dist_forward[v_f], v_f))
        
        # Process backward search (similar logic)
        current_dist_b, u_b = heapq.heappop(heap_backward)
        if u_b in visited_backward:
            continue
        visited_backward.add(u_b)
        
        if u_b in visited_forward:
            shortest_path = min(shortest_path, current_dist_b + dist_forward[u_b])
        
        for v_b, weight_b in graph[u_b]:
            if dist_backward[v_b] > current_dist_b + weight_b:
                dist_backward[v_b] = current_dist_b + weight_b
                heapq.heappush(heap_backward, (dist_backward[v_b], v_b))
    
    return shortest_path