# Dijkstra Algorithm Optimization Toolkit

六种最短路径算法的可运行实现,使用统一 API,附带 benchmark 直接对比性能差异。

**语言**: **简体中文** · [English](./README.en.md)

![Tests](https://github.com/YunhaoDou/dijkstra-algorithm-optimization/actions/workflows/test.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

## 内容

| 算法 | 文件 | 复杂度 | 何时用 |
|------|------|--------|--------|
| 经典 Dijkstra | `src/dijkstra_base.py` | O((V+E) log V) | 单源最短路径、非负权稀疏图通用基线 |
| 双向 Dijkstra | `src/bidirectional.py` | 同上,但常数小很多 | 已知起终点、路径较长 |
| A* | `src/a_star.py` | 同上(最坏),启发函数好时大幅加速 | 有可接受启发函数的场景(网格地图等) |
| Bellman-Ford | `src/bellman_ford.py` | O(V × E) | 含负权;检测负权环(如套利) |
| Floyd-Warshall | `src/floyd_warshall.py` | O(V³) | 小/稠密图,需要所有点对距离 |
| 分层图最短路 | `src/layered_graph.py` | O((V·L)(E·L) log(V·L)) | 带状态约束的问题:"最多 K 次中转"、"时变边权"等 |

六种算法在同一图上**总是返回相同的最短距离**(benchmark 里有断言验证)。区别在**展开了多少节点**。

## 安装

```bash
git clone https://github.com/YunhaoDou/dijkstra-algorithm-optimization
cd dijkstra-algorithm-optimization
```

**无第三方依赖**(核心),Python 3.10+ 标准库即可。

可选:
```bash
pip install matplotlib  # 用于 examples/visualize.py
pip install pytest      # 用 pytest 跑测试(直接 python 跑也行)
```

或作为包安装:
```bash
pip install -e .
```

## 快速上手

```python
from src.dijkstra_base import dijkstra

graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("D", 1)],
    "C": [("B", 2), ("D", 5)],
    "D": [],
}

# 单源全图最短距离
distances = dijkstra(graph, start="A")
# {'A': 0, 'B': 3, 'C': 1, 'D': 4}

# 起终点查询(含路径还原)
path, dist = dijkstra(graph, start="A", end="D")
# path=['A', 'C', 'B', 'D'], dist=4
```

节点可以是任意可哈希类型(int、str、tuple)。

## 跑测试

```bash
# 不需要 pytest
for f in tests/test_*.py; do python "$f"; done

# 装了 pytest 也行
python -m pytest tests/
```

预期输出:
```
test_a_star: OK
test_bellman_ford: OK
test_bidirectional: OK
test_dijkstra: OK
test_floyd_warshall: OK
test_layered: OK
```

CI 会在 Python 3.10、3.11、3.12 上自动跑所有测试。

## 跑示例

```bash
python examples/basic_usage.py       # 简单图上的基础用法
python examples/road_network.py      # A* 在 20x20 网格上找路
python examples/time_expanded.py     # 分层图:最多 K 次中转的最便宜机票
python examples/visualize.py         # 画图对比 Dijkstra 与 A* 的探索范围
```

`visualize.py` 会输出 `visualization.png`,显示两种算法**实际展开了多少格**——A* 在起终点距离远的网格上展开范围明显更小。

## 跑 Benchmark

```bash
python benchmark.py
```

样例输出(M1 Mac):

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

### 一个反直觉的观察

在**小尺寸、低权重方差的均匀网格**上,简单 Dijkstra 反而比 A* 和双向 Dijkstra 略快。原因:

- 启发函数本身有计算开销
- 双向需要维护两套堆和反向图
- 当图很小且权重均匀,优化的"省下的节点"还不够抵消额外开销

**何时优化才真正奏效?**

- 双向 Dijkstra:大图、长路径
- A*:有信息量大的启发函数(如地图上的直线距离),且目标偏离起点很远
- 分层图:**不是为了加速**,是为了表达 Dijkstra 本来无法表达的约束(状态、时间)
- Bellman-Ford:**只在需要负权或检测负权环时用**(套利检测的经典应用)。其他情况都比 Dijkstra 慢。
- Floyd-Warshall:稠密图、需要所有点对距离时有优势;稀疏图上不如跑 N 次 Dijkstra。

这是这个 toolkit 想传递的核心信息:**算法选择应该按问题结构,不是按"听起来更高级"。**

## 分层图最短路简介

很多看起来"超出 Dijkstra 能力"的问题,本质上都是在带状态的图上跑 Dijkstra。

例:**"最多 1 次中转,北京飞香港的最便宜机票"** — 状态是 `(当前城市, 已用航段数)`。

```python
def edges(state):
    city, segments = state
    if segments >= MAX_STOPS + 1:
        return
    for dest, price in flights[city]:
        yield (dest, segments + 1), price

path, cost = layered_shortest_path(edges, ("BJ", 0), lambda s: s[0] == "HK")
```

完整例子见 `examples/time_expanded.py`。

## 项目结构

```
dijkstra-algorithm-optimization/
├── README.md / README.en.md
├── LICENSE / pyproject.toml / requirements.txt
├── benchmark.py             # 6 种算法在同一组图上对比
├── .github/workflows/test.yml   # CI: 多版本 Python 自动跑测试
├── src/
│   ├── dijkstra_base.py     # 基线
│   ├── bidirectional.py     # 双向搜索
│   ├── a_star.py            # 可注入启发函数
│   ├── bellman_ford.py      # 支持负权 + 负环检测
│   ├── floyd_warshall.py    # 全源最短路
│   ├── layered_graph.py     # 状态扩展图上的最短路
│   └── utils.py             # 图校验、反图、随机图/网格图生成
├── examples/
│   ├── basic_usage.py
│   ├── road_network.py
│   ├── time_expanded.py
│   └── visualize.py         # 可视化探索范围对比
└── tests/
    ├── test_dijkstra.py
    ├── test_bidirectional.py
    ├── test_a_star.py
    ├── test_bellman_ford.py
    ├── test_floyd_warshall.py
    └── test_layered.py
```

## 许可

[MIT](LICENSE)
