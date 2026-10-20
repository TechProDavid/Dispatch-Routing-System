import unittest

from ambulance_dispatch.network import (
    create_incident_queue,
    create_incidents,
    create_priority_map,
    create_road_graph,
)


class NetworkTests(unittest.TestCase):
    def test_graph_combines_travel_time_and_delay(self):
        rows = [{
            "Start": "Station",
            "End": "Hospital",
            "Distance": "2.0",
            "Travel Time": "4.5",
            "Traffic Delay": "1.5",
        }]

        graph = create_road_graph(rows)
        self.assertEqual(graph["Station"], [("Hospital", 6.0)])

    def test_incident_heap_places_critical_call_first(self):
        incidents = create_incidents([
            {"Call ID": "2", "Location": "B", "Call Type": "Routine"},
            {"Call ID": "1", "Location": "A", "Call Type": "Critical"},
        ])
        priorities = create_priority_map([
            {"Call Type": "Critical", "Priority": "1"},
            {"Call Type": "Routine", "Priority": "3"},
        ])

        queue = create_incident_queue(incidents, priorities)
        self.assertEqual(queue[0], (1, 1))


if __name__ == "__main__":
    unittest.main()
