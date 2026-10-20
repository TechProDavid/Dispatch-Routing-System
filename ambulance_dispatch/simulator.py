from pathlib import Path

from ambulance_dispatch.dispatch_engine import (
    find_best_unit,
    mark_dispatched,
    return_to_base,
    take_next_incident,
)
from ambulance_dispatch.dispatch_log import (
    append_dispatch_record,
    make_dispatch_record,
)
from ambulance_dispatch.io_utils import read_csv_rows
from ambulance_dispatch.network import (
    create_fleet,
    create_incident_queue,
    create_incidents,
    create_priority_map,
    create_road_graph,
)
from ambulance_dispatch.routing import choose_algorithm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIRECTORY = PROJECT_ROOT / "data"
DEFAULT_RESULTS_DIRECTORY = PROJECT_ROOT / "results"


def prepare_simulation(data_directory=DEFAULT_DATA_DIRECTORY):
    data_directory = Path(data_directory)

    road_rows = read_csv_rows(data_directory / "location_network.csv")
    fleet_rows = read_csv_rows(data_directory / "ambulances.csv")
    incident_rows = read_csv_rows(data_directory / "emergency_calls.csv")
    priority_rows = read_csv_rows(data_directory / "call_priorities.csv")

    road_graph = create_road_graph(road_rows)
    fleet = create_fleet(fleet_rows)
    incidents = create_incidents(incident_rows)
    priority_map = create_priority_map(priority_rows)
    incident_queue = create_incident_queue(incidents, priority_map)

    return road_graph, fleet, incidents, incident_queue


def run_dispatch_simulation(
        algorithm="dijkstra",
        data_directory=DEFAULT_DATA_DIRECTORY,
        log_file=None,
        show_summary=True,
):
    road_graph, fleet, incidents, incident_queue = prepare_simulation(
        data_directory
    )
    routing_algorithm = choose_algorithm(algorithm)

    if log_file is None:
        safe_name = algorithm.lower().replace("-", "_")
        log_file = DEFAULT_RESULTS_DIRECTORY / f"dispatch_log_{safe_name}.csv"

    log_file = Path(log_file)

    if log_file.exists():
        log_file.unlink()

    total_routing_time_ns = 0
    completed_dispatches = 0

    while incident_queue:
        priority, incident_id, incident = take_next_incident(
            incident_queue,
            incidents,
        )

        (
            unit_id,
            route,
            response_time,
            routing_time_ns,
        ) = find_best_unit(
            road_graph,
            fleet,
            incident["location"],
            routing_algorithm,
        )

        total_routing_time_ns += routing_time_ns

        if unit_id is None:
            continue

        mark_dispatched(unit_id, fleet, incident["location"])

        record = make_dispatch_record(
            incident_id,
            priority,
            incident,
            unit_id,
            route,
            response_time,
        )
        append_dispatch_record(record, log_file)
        return_to_base(unit_id, fleet)
        completed_dispatches += 1

    total_routing_time_ms = total_routing_time_ns / 1_000_000

    if show_summary:
        print(f"Routing Algorithm: {algorithm}")
        print(f"Emergency Calls Processed: {completed_dispatches}")
        print(
            "Total Route Processing Time (Nanoseconds):",
            total_routing_time_ns,
            "ns",
        )
        print(
            "Total Route Processing Time (Milliseconds):",
            round(total_routing_time_ms, 6),
            "ms",
        )
        print(f"Dispatch Log: {log_file}")

    return {
        "algorithm": algorithm,
        "calls_processed": completed_dispatches,
        "total_route_time_ns": total_routing_time_ns,
        "total_route_time_ms": total_routing_time_ms,
        "log_path": str(log_file),
    }
