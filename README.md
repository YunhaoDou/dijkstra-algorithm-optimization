# Dijkstra Algorithm Optimization Toolkit

## Overview
This project provides optimized implementations of Dijkstra's algorithm and its variants, including:
- Basic Dijkstra (Priority Queue)
- Bidirectional Dijkstra
- A* Algorithm
- Layered Graph Optimization

## Features
- High-performance implementations in Python
- Modular design for easy extension
- Comprehensive test cases
- Example usage scenarios

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from src.dijkstra_base import Dijkstra

# Initialize with your graph
dijkstra = Dijkstra(graph)
shortest_path = dijkstra.find_path(start, end)
```

## Contributing
Pull requests are welcome. Please ensure tests pass before submitting.

## License
MIT