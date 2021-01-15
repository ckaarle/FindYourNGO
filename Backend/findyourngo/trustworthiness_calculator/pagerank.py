from typing import Tuple, List, Iterable, Dict

from findyourngo.restapi.models import Ngo, NgoConnection
import networkx as nx


class PageRank:

    def __init__(self, ngos: Iterable[Ngo]):
        self.ngos = ngos
        self.G = nx.DiGraph()

        self.initialized = False

    def make_graph(self):
        nodes, edges = self.make_nodes_and_edges()

        self.G.add_nodes_from(nodes)

        for edge in edges:
            self.G.add_edge(*edge)

    def make_nodes_and_edges(self) -> Tuple[List[Tuple[str, Dict[str, float]]], List[Tuple[str, str]]]:
        edges = []
        nodes = []

        for ngo in self.ngos:
            connected_ngos = self._get_connected_ngos(ngo)

            if connected_ngos:
                nodes.append((ngo.name, {'tw': ngo.tw_score.total_tw_score}))
                for connected_ngo in connected_ngos:
                    edges.append((ngo.name, connected_ngo.name))

        return nodes, edges

    def pagerank(self, alpha: float = 0.85) -> Dict[str, float]:
        self._initialize()
        return nx.pagerank(self.G, alpha=alpha)

    def personalized_pagerank(self, alpha: float = 0.85) -> Dict[str, float]:
        self._initialize()
        personalization = self._get_personalization()
        return nx.pagerank(self.G, alpha=alpha, personalization=personalization)

    def _get_connected_ngos(self, ngo):
        return NgoConnection.objects.filter(reporter_id=ngo.id)

    def _get_personalization(self) -> Dict[str, float]:
        connected_tw_sum = {}
        for ngo in self.ngos:
            connected_ngos = self._get_connected_ngos(ngo)
            connected_tw_sum[ngo.name] = sum(map(lambda ngo: ngo.tw_score.total_tw_score, connected_ngos))

        total_tw = sum(connected_tw_sum.values())

        connected_tw_sum_percentage = {
            ngo_name: tw_score / total_tw for ngo_name, tw_score in connected_tw_sum.items()
        }

        return connected_tw_sum_percentage

    def _initialize(self):
        if not self.initialized:
            self.make_graph()
            self.initialized = True

    def draw_graph(self):
        self._initialize()
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