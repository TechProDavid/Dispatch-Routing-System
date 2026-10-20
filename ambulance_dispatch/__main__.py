import argparse

from ambulance_dispatch.simulator import run_dispatch_simulation


def get_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Priority-based ambulance dispatch simulation with "
            "Dijkstra and Bellman-Ford routing."
        )
    )
    parser.add_argument(
        "--algorithm",
        choices=["dijkstra", "bellman-ford"],
        default="dijkstra",
    )
    parser.add_argument(
        "--log",
        default=None,
        help="Optional output path for the dispatch CSV log.",
    )
    return parser.parse_args()


def main():
    arguments = get_arguments()
    run_dispatch_simulation(
        algorithm=arguments.algorithm,
        log_file=arguments.log,
    )


if __name__ == "__main__":
    main()
