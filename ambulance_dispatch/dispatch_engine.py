# Queue processing and response-unit selection.
import heapq

from ambulance_dispatch.timing import begin_timer, elapsed_nanoseconds


def take_next_incident(incident_queue, incidents):
    priority, incident_id = heapq.heappop(incident_queue)
    return priority, incident_id, incidents[incident_id]


def find_best_unit(graph, fleet, destination, routing_algorithm):
    candidates = {}
    start_time = begin_timer()

    for unit_id, unit in fleet.items():
        if not unit["available"]:
            continue

        route, response_time = routing_algorithm(
            graph,
            unit["location"],
            destination,
        )

        if not route:
            continue

        candidates[unit_id] = {
            "route": route,
            "response_time": response_time,
        }

    routing_time_ns = elapsed_nanoseconds(start_time)

    if not candidates:
        return None, [], float("inf"), routing_time_ns

    selected_unit = min(
        candidates,
        key=lambda unit_id: candidates[unit_id]["response_time"],
    )

    return (
        selected_unit,
        candidates[selected_unit]["route"],
        candidates[selected_unit]["response_time"],
        routing_time_ns,
    )


def mark_dispatched(unit_id, fleet, destination):
    fleet[unit_id]["available"] = False
    fleet[unit_id]["location"] = destination


def return_to_base(unit_id, fleet):
    fleet[unit_id]["location"] = fleet[unit_id]["home_base"]
    fleet[unit_id]["available"] = True
