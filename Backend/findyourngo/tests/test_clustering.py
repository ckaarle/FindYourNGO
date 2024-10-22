from unittest import TestCase

from collections import namedtuple
from findyourngo.restapi.map_utils import get_links_between_ngos


def ngo(id, long, lat):
    Ngo = namedtuple('Ngo', ['id', 'name', 'contact'])
    Contact = namedtuple('Contact', ['address'])
    Address = namedtuple('Address', ['latitude', 'longitude'])
    return Ngo(id, id, Contact(Address(lat, long)))


def create_connections(pairs: [(int, int)]):
    Connection = namedtuple('Connection', ['reporter_id', 'connected_ngo_id'])
    connections = []
    for pair in pairs:
        connections.append(Connection(pair[0], pair[1]))
        connections.append(Connection(pair[1], pair[0]))
    return connections


def cluster(c_id, lng_min, lng_max, lat_min, lat_max):
    return {'id': c_id, 'lng_min': lng_min, 'lng_max': lng_max, 'lat_min': lat_min, 'lat_max': lat_max}


def common_body(clusters):
    ngos = [
        ngo(0, 1, 1),
        ngo(1, 2, 2),
        ngo(2, 11, 1),
    ]
    connections = create_connections([
        (0, 1),
        (0, 2),
        (1, 2),
    ])

    return get_links_between_ngos(clusters, ngos, connections)


class TestClusteringMethods(TestCase):
    def test_simple_case(self):
        clusters = [
            cluster(0, 0, 10, 0, 10),
            cluster(1, 10, 20, 0, 10),
        ]

        result = common_body(clusters)

        expected_links = {
            ((5, 5), (15, 5)): 2,
        }
        self.assertEqual(expected_links, result)

    def test_no_clusters(self):
        # request object should never send None to this function
        result = common_body([])

        expected_links = {}
        self.assertEqual(expected_links, result)

    def test_empty_clusters(self):
        clusters = [
            cluster(0, 0, 0, 0, 0),
            cluster(1, 0, 0, 0, 0),
        ]

        result = common_body(clusters)

        expected_links = {
            ((0, 0), (0, 0)): 0,
        }
        self.assertEqual(expected_links, result)

    def test_intersecting_clusters(self):
        clusters = [
            cluster(0, 0, 20, 0, 10),
            cluster(1, 10, 20, 0, 10),
        ]

        result = common_body(clusters)

        expected_links = {
            ((10, 5), (15, 5)): 0,
        }
        self.assertEqual(expected_links, result)
