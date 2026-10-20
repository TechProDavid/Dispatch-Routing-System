# CSV output for completed simulated dispatches.
import csv
from pathlib import Path


FIELD_NAMES = [
    "Call ID",
    "Priority",
    "Emergency",
    "Call Location",
    "Selected Ambulance",
    "Route",
    "Estimated Travel Time",
]


def make_dispatch_record(
        incident_id,
        priority,
        incident,
        unit_id,
        route,
        response_time,
):
    return {
        "Call ID": incident_id,
        "Priority": priority,
        "Emergency": incident["type"],
        "Call Location": incident["location"],
        "Selected Ambulance": unit_id,
        "Route": " -> ".join(route),
        "Estimated Travel Time": response_time,
    }


def append_dispatch_record(record, filename):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not path.exists()

    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)

        if needs_header:
            writer.writeheader()

        writer.writerow(record)
