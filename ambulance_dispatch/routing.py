# Two shortest-path implementations for the same weighted road graph.
import heapq


def dijkstra_shortest_path(graph, source, destination):
    best_time = {location: float("inf") for location in graph}
    best_time[source] = 0
    parent = {location: None for location in graph}
    pending = [(0, source)]

    while pending:
        current_time, current_location = heapq.heappop(pending)

        if current_time != best_time[current_location]:
            continue

        if current_location == destination:
            break

        for neighbor, edge_time in graph[current_location]:
            candidate_time = current_time + edge_time

            if candidate_time < best_time[neighbor]:
                best_time[neighbor] = candidate_time
                parent[neighbor] = current_location
                heapq.heappush(pending, (candidate_time, neighbor))

    return _build_route_result(best_time, parent, destination)


def bellman_ford_shortest_path(graph, source, destination):
    best_time = {location: float("inf") for location in graph}
    best_time[source] = 0
    parent = {location: None for location in graph}

    for _ in range(len(graph) - 1):
        changed = False

        for origin, connections in graph.items():
            if best_time[origin] == float("inf"):
                continue

            for neighbor, edge_time in connections:
                candidate_time = best_time[origin] + edge_time

                if candidate_time < best_time[neighbor]:
                    best_time[neighbor] = candidate_time
                    parent[neighbor] = origin
                    changed = True

        if not changed:
            break

    return _build_route_result(best_time, parent, destination)


def _build_route_result(best_time, parent, destination):
    if best_time[destination] == float("inf"):
        return [], float("inf")

    route = []
    location = destination

    while location is not None:
        route.append(location)
        location = parent[location]

    route.reverse()
    return route, round(best_time[destination], 2)


def choose_algorithm(name):
    normalized_name = name.lower().replace("_", "-")

    if normalized_name == "dijkstra":
        return dijkstra_shortest_path

    if normalized_name in {"bellman-ford", "bellmanford"}:
        return bellman_ford_shortest_path

    raise ValueError("Choose either 'dijkstra' or 'bellman-ford'.")
