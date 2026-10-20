import argparse
import csv
import random
from pathlib import Path


LOCATIONS = [
    "Central Station",
    "North Clinic",
    "River Junction",
    "East Market",
    "South Park",
    "West Gate",
    "Lakeside Center",
]

CALL_PRIORITIES = [
    ("Cardiac Arrest", 1),
    ("Stroke Symptoms", 1),
    ("Major Collision", 1),
    ("Structure Fire", 1),
    ("Labor Emergency", 1),
    ("Drug Overdose", 1),
    ("Respiratory Distress", 1),
    ("Severe Hemorrhage", 1),
    ("Head Trauma", 1),
    ("Seizure", 1),
    ("Minor Collision", 2),
    ("Allergic Reaction", 2),
    ("Suspected Fracture", 2),
    ("Syncope", 2),
    ("Animal Injury", 2),
    ("Minor Burn", 3),
    ("Gastrointestinal Illness", 3),
    ("Persistent Fever", 3),
    ("Dehydration", 3),
    ("Anxiety Episode", 3),
]


def write_road_network(output_directory, generator):
    filename = output_directory / "location_network.csv"

    with filename.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Start",
            "End",
            "Distance",
            "Travel Time",
            "Traffic Delay",
        ])

        for origin in LOCATIONS:
            for destination in LOCATIONS:
                if origin == destination:
                    continue

                distance = round(generator.uniform(0.7, 5.2), 2)
                travel_time = round(
                    distance * generator.uniform(1.7, 2.3),
                    2,
                )
                traffic_delay = round(generator.uniform(0.0, 4.5), 2)

                writer.writerow([
                    origin,
                    destination,
                    distance,
                    travel_time,
                    traffic_delay,
                ])


def write_fleet(output_directory):
    filename = output_directory / "ambulances.csv"

    with filename.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Ambulance ID", "Staging Location"])
        writer.writerows([
            ["Medic 1", "Central Station"],
            ["Medic 2", "North Clinic"],
            ["Medic 3", "South Park"],
        ])


def write_priorities(output_directory):
    filename = output_directory / "call_priorities.csv"

    with filename.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Call Type", "Priority"])
        writer.writerows(CALL_PRIORITIES)


def write_emergency_calls(output_directory, generator):
    filename = output_directory / "emergency_calls.csv"
    call_types = [call_type for call_type, _ in CALL_PRIORITIES]

    with filename.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Call ID", "Location", "Call Type"])

        for call_id in range(1, 101):
            writer.writerow([
                call_id,
                generator.choice(LOCATIONS),
                generator.choice(call_types),
            ])


def generate_dataset(output_directory, seed):
    output_directory.mkdir(parents=True, exist_ok=True)
    generator = random.Random(seed)

    write_road_network(output_directory, generator)
    write_fleet(output_directory)
    write_priorities(output_directory)
    write_emergency_calls(output_directory, generator)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data"),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=7952026,
    )
    arguments = parser.parse_args()

    generate_dataset(arguments.output, arguments.seed)
    print(f"Synthetic dataset written to: {arguments.output.resolve()}")


if __name__ == "__main__":
    main()
