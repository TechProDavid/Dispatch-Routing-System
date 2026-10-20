import unittest

from ambulance_dispatch.dispatch_engine import find_best_unit
from ambulance_dispatch.routing import dijkstra_shortest_path


class DispatchEngineTests(unittest.TestCase):
    def test_fastest_available_unit_is_selected(self):
        graph = {
            "Station A": [("Call Site", 4.0)],
            "Station B": [("Call Site", 2.0)],
            "Call Site": [],
        }
        fleet = {
            "Medic 1": {
                "home_base": "Station A",
                "location": "Station A",
                "available": True,
            },
            "Medic 2": {
                "home_base": "Station B",
                "location": "Station B",
                "available": True,
            },
        }

        unit_id, route, response_time, _ = find_best_unit(
            graph,
            fleet,
            "Call Site",
            dijkstra_shortest_path,
        )

        self.assertEqual(unit_id, "Medic 2")
        self.assertEqual(route, ["Station B", "Call Site"])
        self.assertEqual(response_time, 2.0)

    def test_unavailable_unit_is_ignored(self):
        graph = {
            "Station A": [("Call Site", 1.0)],
            "Station B": [("Call Site", 3.0)],
            "Call Site": [],
        }
        fleet = {
            "Medic 1": {
                "home_base": "Station A",
                "location": "Station A",
                "available": False,
            },
            "Medic 2": {
                "home_base": "Station B",
                "location": "Station B",
                "available": True,
            },
        }

        unit_id, _, response_time, _ = find_best_unit(
            graph,
            fleet,
            "Call Site",
            dijkstra_shortest_path,
        )

        self.assertEqual(unit_id, "Medic 2")
        self.assertEqual(response_time, 3.0)


if __name__ == "__main__":
    unittest.main()
