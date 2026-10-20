# Small CSV helper used by the simulator.
import csv
from pathlib import Path


def read_csv_rows(filename):
    path = Path(filename)

    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))
