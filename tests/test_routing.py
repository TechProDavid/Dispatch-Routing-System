import unittest

from ambulance_dispatch.routing import (
    bellman_ford_shortest_path,
    dijkstra_shortest_path,
)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "A": [("B", 2.0), ("C", 8.0)],
            "B": [("C", 3.0), ("D", 7.0)],
            "C": [("D", 1.0)],
            "D": [],
        }

    def test_dijkstra_finds_shortest_path(self):
        route, travel_time = dijkstra_shortest_path(self.graph, "A", "D")
        self.assertEqual(route, ["A", "B", "C", "D"])
        self.assertEqual(travel_time, 6.0)

    def test_bellman_ford_finds_shortest_path(self):
        route, travel_time = bellman_ford_shortest_path(
            self.graph,
            "A",
            "D",
        )
        self.assertEqual(route, ["A", "B", "C", "D"])
        self.assertEqual(travel_time, 6.0)

    def test_algorithms_agree_on_path_cost(self):
        _, dijkstra_time = dijkstra_shortest_path(self.graph, "A", "D")
        _, bellman_time = bellman_ford_shortest_path(self.graph, "A", "D")
        self.assertEqual(dijkstra_time, bellman_time)


if __name__ == "__main__":
    unittest.main()
