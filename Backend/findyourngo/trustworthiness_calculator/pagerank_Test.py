import itertools
import pprint
import random

import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt

from findyourngo.restapi.models import Ngo, NgoTWScore
from findyourngo.trustworthiness_calculator.pagerank import PageRank


def test_pagerank_library_function():
    nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    # Generate Networkx Graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)

    G.add_edge('a', 'h')
    G.add_edge('b', 'h')
    G.add_edge('c', 'h')
    G.add_edge('d', 'h')
    G.add_edge('h', 'e')
    G.add_edge('h', 'f')
    G.add_edge('h', 'g')
    G.add_edge('e', 'a')
    G.add_edge('e', 'b')
    G.add_edge('e', 'c')
    G.add_edge('e', 'd')
    G.add_edge('f', 'h')
    G.add_edge('g', 'h')

    # Draw generated graph
    nx.draw_networkx(G, pos=nx.circular_layout(G), with_labels=True, arrows=True)

    # Compute Page Rank
    ppr = nx.pagerank(G, alpha=0.85)
    pprint.pprint(ppr)

    assert ppr['a'] == 0.047292036113501794
    assert ppr['b'] == 0.047292036113501794
    assert ppr['c'] == 0.047292036113501794
    assert ppr['d'] == 0.047292036113501794

    assert ppr['e'] == 0.1343164861335311
    assert ppr['f'] == 0.1343164861335311
    assert ppr['g'] == 0.1343164861335311

    assert ppr['h'] == 0.40788239714539937

    plt.show()


def test_personalized_pagerank_library_function():
    fraud = pd.DataFrame({
        'individual': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
        'fraudster': [1, 0, 0, 0, 1, 0, 0, 0]
    })

    # Generate Networkx Graph
    G = nx.Graph()
    G.add_nodes_from(fraud['individual'])

    # randomly determine vertices
    for (node1, node2) in itertools.combinations(fraud['individual'], 2):
        if random.random() < 0.5:
            G.add_edge(node1, node2)

    # Draw generated graph
    nx.draw_networkx(G, pos=nx.circular_layout(G), with_labels=True)

    # Compute Personalized Page Rank
    personalization = fraud.set_index('individual')['fraudster'].to_dict()
    ppr = nx.pagerank(G, alpha=0.85, personalization=personalization)
    pprint.pprint(ppr)

    plt.show()


ngo_a = Ngo(name='a', tw_score=NgoTWScore(total_tw_score=1))
ngo_b = Ngo(name='b', tw_score=NgoTWScore(total_tw_score=0))
ngo_c = Ngo(name='c', tw_score=NgoTWScore(total_tw_score=3))
ngo_d = Ngo(name='d', tw_score=NgoTWScore(total_tw_score=2.5))
ngo_e = Ngo(name='e', tw_score=NgoTWScore(total_tw_score=4.5))
ngo_f = Ngo(name='f', tw_score=NgoTWScore(total_tw_score=2))
ngo_g = Ngo(name='g', tw_score=NgoTWScore(total_tw_score=3))
ngo_h = Ngo(name='h', tw_score=NgoTWScore(total_tw_score=5))

ngo_i = Ngo(name='i', tw_score=NgoTWScore(total_tw_score=0))
ngo_j = Ngo(name='j', tw_score=NgoTWScore(total_tw_score=0.3))
ngo_k = Ngo(name='k', tw_score=NgoTWScore(total_tw_score=0))
ngo_l = Ngo(name='l', tw_score=NgoTWScore(total_tw_score=0.5))

ngos = [
    ngo_a, ngo_b, ngo_c, ngo_d,
    ngo_e, ngo_f, ngo_g, ngo_h,
             ]

ngos_with_subgraph = [
    ngo_a, ngo_b, ngo_c, ngo_d,
    ngo_e, ngo_f, ngo_g, ngo_h,
    ngo_i, ngo_j, ngo_k, ngo_l,
             ]

ngos_by_name = {
    'a': ngo_a,
    'b': ngo_b,
    'c': ngo_c,
    'd': ngo_d,
    'e': ngo_e,
    'f': ngo_f,
    'g': ngo_g,
    'h': ngo_h,
    'i': ngo_i,
    'j': ngo_j,
    'k': ngo_k,
    'l': ngo_l,
}


class PageRankTest(PageRank):

    def __init__(self, ngos):
        super().__init__(ngos)
        self.connected = {
            'a': ['h', 'e'],
            'b': ['h', 'e'],
            'c': ['h', 'e'],
            'd': ['h', 'e'],
            'e': ['a', 'b', 'c', 'd', 'h'],
            'f': ['h'],
            'g': ['h'],
            'h': ['e', 'f', 'g', 'a', 'b', 'c', 'd'],
        }

    def _get_connected_ngos(self, ngo):
        connected_names = self.connected[ngo.name]

        ngos = []
        for connected_name in connected_names:
            ngos.append(ngos_by_name[connected_name])
        return ngos


def test_pagerank_with_ngos():
    pr = PageRankTest(ngos)
    pr.draw_graph()

    ppr = pr.pagerank()
    pprint.pprint(ppr)

    assert ppr['a'] == 0.09214971509174363
    assert ppr['b'] == 0.09214971509174363
    assert ppr['c'] == 0.09214971509174363
    assert ppr['d'] == 0.09214971509174363

    assert ppr['e'] == 0.2126521415534134
    assert ppr['f'] == 0.05599866179848425
    assert ppr['g'] == 0.05599866179848425

    assert ppr['h'] == 0.30675167448264345

    plt.show()


class PageRankWithSubgraphsTest(PageRankTest):

    def __init__(self, ngos, cancel_subgraph: bool = True):
        super().__init__(ngos)

        self.cancel_subgraph = cancel_subgraph

        self.connected = {
            'a': ['h', 'e'],
            'b': ['h', 'e'],
            'c': ['h', 'e'],
            'd': ['h', 'e'],
            'e': ['a', 'b', 'c', 'd', 'h'],
            'f': ['h'],
            'g': ['h'],
            'h': ['e', 'f', 'g', 'a', 'b', 'c', 'd'],
            'i': ['j', 'l'],
            'j': ['k', 'i'],
            'k': ['l', 'j'],
            'l': ['i', 'k'],
        }


class PageRankWithSubgraphsDefaultPersonalizationTest(PageRankWithSubgraphsTest):

    def _get_personalization(self):
        if self.cancel_subgraph:
            return {
                'a': 1/8,
                'b': 1/8,
                'c': 1/8,
                'd': 1/8,
                'e': 1/8,
                'f': 1/8,
                'g': 1/8,
                'h': 1/8,
            } # i, j, k, l default to 0

        else:
            return {
                'a': 1 / 9,
                'b': 1 / 9,
                'c': 1 / 9,
                'd': 1 / 9,
                'e': 1 / 9,
                'f': 1 / 9,
                'g': 1 / 9,
                'h': 1 / 9,
                'i': (1 / 9) / 4,
                'j': (1 / 9) / 4,
                'k': (1 / 9) / 4,
                'l': (1 / 9) / 4,
            }


def test_pagerank_with_fraudulent_ngo_connections():
    pr = PageRankWithSubgraphsTest(ngos_with_subgraph)
    pr.draw_graph()

    ppr = pr.pagerank()
    pprint.pprint(ppr)

    assert ppr['a'] == 0.061432505304915785
    assert ppr['b'] == 0.061432505304915785
    assert ppr['c'] == 0.061432505304915785
    assert ppr['d'] == 0.061432505304915785

    assert ppr['e'] == 0.14176925997418122
    assert ppr['f'] == 0.03733208170158334
    assert ppr['g'] == 0.03733208170158334

    assert ppr['h'] == 0.2045032220696556 # down from 0.4 without subgraph!

    # fraudulent subgraph
    # higher scores than a, b, c, d from above (not great)
    assert ppr['i'] == 0.08333333333333333
    assert ppr['j'] == 0.08333333333333333
    assert ppr['k'] == 0.08333333333333333
    assert ppr['l'] == 0.08333333333333333

    plt.show()


def test_default_personalized_pagerank_with_ngos_cancel_subgraph():
    pr = PageRankWithSubgraphsDefaultPersonalizationTest(ngos_with_subgraph, cancel_subgraph=True)
    pr.draw_graph()

    ppr = pr.personalized_pagerank()
    pprint.pprint(ppr)

    assert ppr['a'] == 0.09214658850314891 # essentially the same as without subgraph
    assert ppr['b'] == 0.09214658850314891
    assert ppr['c'] == 0.09214658850314891
    assert ppr['d'] == 0.09214658850314891

    assert ppr['e'] == 0.2126454214506791
    assert ppr['f'] == 0.055997082439816076
    assert ppr['g'] == 0.055997082439816076

    assert ppr['h'] == 0.3067424545321898

    # fraudulent subgraph
    # tiny scores
    assert ppr['i'] == 7.901281225791675e-06
    assert ppr['j'] == 7.901281225791675e-06
    assert ppr['k'] == 7.901281225791675e-06
    assert ppr['l'] == 7.901281225791675e-06

    plt.show()


def test_default_personalized_pagerank_with_ngos_reduce_subgraph():
    pr = PageRankWithSubgraphsDefaultPersonalizationTest(ngos_with_subgraph, cancel_subgraph=False)
    pr.draw_graph()

    ppr = pr.personalized_pagerank()
    pprint.pprint(ppr)

    assert ppr['a'] == 0.08190798131958271 # similar to without subgraph
    assert ppr['b'] == 0.08190798131958271
    assert ppr['c'] == 0.08190798131958271
    assert ppr['d'] == 0.08190798131958271

    assert ppr['e'] == 0.18901790963480697
    assert ppr['f'] == 0.04977513570708415
    assert ppr['g'] == 0.04977513570708415

    assert ppr['h'] == 0.2726596198165738

    # fraudulent subgraph
    # small(er) scores
    assert ppr['i'] == 0.027785068464029936 # down from 0.0833...
    assert ppr['j'] == 0.027785068464029936
    assert ppr['k'] == 0.027785068464029936
    assert ppr['l'] == 0.027785068464029936

    plt.show()


def test_personalized_pagerank_without_fraudulent_ngo_connections():
    pr = PageRankTest(ngos)
    pr.draw_graph()

    ppr = pr.personalized_pagerank()
    pprint.pprint(ppr)

    assert ppr['a'] == 0.09385927392467
    assert ppr['b'] == 0.09385927392467
    assert ppr['c'] == 0.09385927392467
    assert ppr['d'] == 0.09385927392467

    assert ppr['e'] == 0.21999339905537146
    assert ppr['f'] == 0.04751980216757451
    assert ppr['g'] == 0.04751980216757451

    assert ppr['h'] == 0.3095299009107994

    plt.show()


def test_personalized_pagerank_with_fraudulent_ngo_connections():
    pr = PageRankWithSubgraphsTest(ngos_with_subgraph)
    pr.draw_graph()

    ppr = pr.personalized_pagerank()
    pprint.pprint(ppr)
    # plt.savefig('ngos.png')

    assert ppr['a'] == 0.09190852886920517
    assert ppr['b'] == 0.09190852886920517
    assert ppr['c'] == 0.09190852886920517
    assert ppr['d'] == 0.09190852886920517

    assert ppr['e'] == 0.21542177175607552
    assert ppr['f'] == 0.04653216603094387
    assert ppr['g'] == 0.04653216603094387

    assert ppr['h'] == 0.30309787343504085

    assert ppr['i'] == 0.005616170819173685
    assert ppr['j'] == 0.00477478281591386
    assert ppr['k'] == 0.005616170819173685
    assert ppr['l'] == 0.00477478281591386

    plt.show()