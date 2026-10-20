# Build the in-memory structures used by the dispatch simulation.
import heapq


def create_road_graph(rows):
    road_graph = {}

    for row in rows:
        origin = row["Start"]
        destination = row["End"]
        base_time = float(row["Travel Time"])
        delay = float(row["Traffic Delay"])
        route_cost = round(base_time + delay, 2)

        road_graph.setdefault(origin, [])
        road_graph.setdefault(destination, [])
        road_graph[origin].append((destination, route_cost))

    return road_graph


def create_fleet(rows):
    fleet = {}

    for row in rows:
        unit_id = row["Ambulance ID"]
        home_base = row["Staging Location"]

        fleet[unit_id] = {
            "home_base": home_base,
            "location": home_base,
            "available": True,
        }

    return fleet


def create_incidents(rows):
    incidents = {}

    for row in rows:
        incident_id = int(row["Call ID"])
        incidents[incident_id] = {
            "location": row["Location"],
            "type": row["Call Type"],
        }

    return incidents


def create_priority_map(rows):
    priority_map = {}

    for row in rows:
        priority_map[row["Call Type"]] = int(row["Priority"])

    return priority_map


def create_incident_queue(incidents, priority_map):
    incident_queue = []

    for incident_id, incident in incidents.items():
        incident_type = incident["type"]

        if incident_type not in priority_map:
            raise ValueError(f"No priority configured for: {incident_type}")

        heapq.heappush(
            incident_queue,
            (priority_map[incident_type], incident_id),
        )

    return incident_queue
