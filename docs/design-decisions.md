# Design Decisions

## Adjacency-list graph

The road network is stored as a dictionary where each location maps to a list of outgoing `(destination, weight)` edges. This keeps graph traversal direct and readable.

## Effective routing weight

Each edge uses:

`effective weight = travel time + traffic delay`

This keeps the simulation simple while allowing congestion to affect route selection.

## Heap-based call queue

Emergency calls are stored in Python's `heapq` as `(priority, call_id)` tuples. Lower numeric priority values represent more urgent calls. The call ID provides deterministic ordering when two calls share the same priority.

## Fastest-ambulance selection

The simulator calculates a route from every available ambulance to the current emergency location, stores each candidate route and travel time, and chooses the ambulance with the minimum estimated response time.

## Stateless response cycle

After a response is logged, the ambulance returns to its configured staging location and becomes available again. This isolates routing performance from fleet-utilization modeling and keeps the project focused on data structures and algorithms.

## Synthetic data

All committed road, ambulance, and emergency-call data was generated specifically for this public portfolio project. It contains no operational EMS information, patient information, or private datasets.
