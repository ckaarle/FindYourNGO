from typing import Tuple, List, Iterable, Dict, Optional

from findyourngo.restapi.models import Ngo, NgoConnection
import networkx as nx


class PageRank:

    def __init__(self, ngos: Iterable[Ngo]):
        self.G = nx.DiGraph()
        self._initialize(ngos)

    def make_graph(self):
        self.G.add_nodes_from(self.nodes)

        for edge in self.edges:
            self.G.add_edge(*edge)

    def _pagerank(self, alpha: float = 0.85) -> Dict[str, float]:
        return nx.pagerank(self.G, alpha=alpha)

    def personalized_pagerank(self, alpha: float = 0.85) -> Optional[Dict[str, float]]:
        if not self.G.nodes: # graph is empty
            return None

        return nx.pagerank(self.G, alpha=alpha, personalization=self.personalization)

    def _get_connected_ngos(self, ngo):
        return NgoConnection.objects.filter(reporter_id=ngo.id)

    def draw_graph(self):
        nx.draw_networkx(self.G, pos=nx.circular_layout(self.G), with_labels=True, arrows=True)

        # to add the tw to the graph, uncomment the following
        # labels = nx.get_node_attributes(self.G, 'tw')
        # nx.draw_networkx_labels(self.G, pos={
        #     'a': [1.05, 0.1],
        #     'b': [0.9, 0.6],
        #     'c': [0.6, 0.95],
        #     'd': [0.1, 1.1],
        #     'e': [-0.5, 1],
        #     'f': [-0.9, 0.6],
        #     'g': [-1, 0.135],
        #     'h': [-0.9, -0.65],
        #     'i': [-0.5, -1],
        #     'j': [0, -1.15],
        #     'k': [0.6, -0.95],
        #     'l': [0.9, -0.65],
        # }, labels=labels)

    def _get_percentage(self, tw_score, total_tw):
        if total_tw <= 0:
            return 0

        return tw_score / total_tw

    def _initialize(self, ngos):
        self.edges = []
        self.nodes = []

        connected_tw_sum = {}

        for ngo in ngos:
            connections = self._get_connected_ngos(ngo)

            if not connections:
                continue

            self.nodes.append((ngo.name, {'tw': ngo.tw_score.total_tw_score}))
            for connection in connections:
                self.edges.append((ngo.name, connection.connected_ngo.name))

            connected_tw_sum[ngo.name] = sum(map(lambda connection: connection.connected_ngo.tw_score.total_tw_score, connections))

        total_tw = sum(connected_tw_sum.values())

        self.personalization = {
            ngo_name: self._get_percentage(tw_score, total_tw) for ngo_name, tw_score in connected_tw_sum.items()
        }

        self.make_graph()
