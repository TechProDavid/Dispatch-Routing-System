# Algorithm Comparison

The application supports two shortest-path implementations against the same dispatch workload.

## Dijkstra

Dijkstra uses a min-priority queue to process the next closest vertex. For this project, every road weight is non-negative because each weight represents travel time plus traffic delay.

With an adjacency list and heap-based priority queue, the implementation is appropriate for repeatedly finding shortest routes in a positively weighted road network.

## Bellman-Ford

Bellman-Ford repeatedly relaxes graph edges for up to `V - 1` passes. The implementation exits early when a full pass produces no updates.

Bellman-Ford is more general than required by this synthetic road network because it can support negative edge weights. Road travel time cannot be negative, so that flexibility introduces additional processing work without providing a practical advantage here.

## Benchmark design

The committed benchmark processes the same workload with each algorithm:

- 7 locations
- 42 directed road segments
- 3 ambulances
- 100 emergency calls
- 20 emergency categories
- 3 priority levels
- 10 timed runs per algorithm

Only route-selection processing time is accumulated. File loading and log-writing time are excluded from the routing metric.

See [`results/benchmark_results.csv`](../results/benchmark_results.csv) for the raw measurements.

> Runtime values depend on hardware, operating system, Python version, and background workload. The useful comparison is the relative behavior of both algorithms under the same conditions.
