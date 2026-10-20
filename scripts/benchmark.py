import argparse
import csv
import statistics
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ambulance_dispatch.simulator import run_dispatch_simulation


DEFAULT_OUTPUT = PROJECT_ROOT / "results" / "benchmark_results.csv"


def collect_measurements(algorithm, number_of_runs):
    measurements = []

    for run_number in range(1, number_of_runs + 1):
        log_file = (
            PROJECT_ROOT /
            "results" /
            "benchmark_logs" /
            f"{algorithm.replace('-', '_')}_{run_number}.csv"
        )

        result = run_dispatch_simulation(
            algorithm=algorithm,
            log_file=log_file,
            show_summary=False,
        )
        measurements.append(result["total_route_time_ms"])

    return measurements


def write_measurements(results, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Run", "Route Processing Time (ms)"])

        for algorithm, measurements in results.items():
            for run_number, runtime in enumerate(measurements, start=1):
                writer.writerow([algorithm, run_number, f"{runtime:.6f}"])


def display_summary(results):
    averages = {}
    print("\n--- ROUTING PERFORMANCE COMPARISON ---")

    for algorithm, measurements in results.items():
        averages[algorithm] = statistics.mean(measurements)
        print(f"\n{algorithm.upper()}")

        for run_number, runtime in enumerate(measurements, start=1):
            print(f"Run {run_number}: {runtime:.6f} ms")

        print(f"Average: {averages[algorithm]:.6f} ms")

    dijkstra = averages["dijkstra"]
    bellman_ford = averages["bellman-ford"]
    difference = (bellman_ford - dijkstra) / bellman_ford * 100

    print(
        "\nDijkstra route processing was "
        f"{difference:.2f}% faster than Bellman-Ford "
        "for this benchmark run."
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()

    results = {
        "dijkstra": collect_measurements("dijkstra", arguments.runs),
        "bellman-ford": collect_measurements("bellman-ford", arguments.runs),
    }

    write_measurements(results, arguments.output)
    display_summary(results)
    print(f"\nResults saved to: {arguments.output}")


if __name__ == "__main__":
    main()
