import networkx as nx


class RoutePlanner:

    def __init__(self):

        self.graph = nx.Graph()

        roads = [
            ("Home", "Junction A", 4),
            ("Home", "Junction B", 7),
            ("Junction A", "Junction C", 3),
            ("Junction A", "Junction D", 5),
            ("Junction B", "Junction D", 2),
            ("Junction C", "College", 4),
            ("Junction D", "College", 3),
            ("Junction C", "Hospital", 5),
            ("Junction D", "Hospital", 4),
            ("Hospital", "College", 2)
        ]

        for start, end, distance in roads:

            self.graph.add_edge(
                start,
                end,
                weight=distance
            )

    def find_route(self, start, destination):

        try:

            route = nx.astar_path(
                self.graph,
                start,
                destination,
                weight="weight"
            )

            cost = nx.astar_path_length(
                self.graph,
                start,
                destination,
                weight="weight"
            )

            return route, cost

        except nx.NetworkXNoPath:

            return None, None