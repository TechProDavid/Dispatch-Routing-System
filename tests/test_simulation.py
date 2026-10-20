import csv
import tempfile
import unittest
from pathlib import Path

from ambulance_dispatch.simulator import run_dispatch_simulation


class SimulationTests(unittest.TestCase):
    def test_dijkstra_processes_all_calls_and_creates_log(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_file = Path(temporary_directory) / "dispatch.csv"
            result = run_dispatch_simulation(
                algorithm="dijkstra",
                log_file=log_file,
                show_summary=False,
            )

            self.assertEqual(result["calls_processed"], 100)
            self.assertTrue(log_file.exists())

            with log_file.open("r", newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))

            self.assertEqual(len(rows), 100)

    def test_both_algorithms_complete_the_same_workload(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)

            dijkstra = run_dispatch_simulation(
                algorithm="dijkstra",
                log_file=directory / "dijkstra.csv",
                show_summary=False,
            )
            bellman_ford = run_dispatch_simulation(
                algorithm="bellman-ford",
                log_file=directory / "bellman.csv",
                show_summary=False,
            )

            self.assertEqual(
                dijkstra["calls_processed"],
                bellman_ford["calls_processed"],
            )


if __name__ == "__main__":
    unittest.main()
