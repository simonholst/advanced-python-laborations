import copy
import unittest
from pprint import pprint

from hypothesis import given, strategies as st

from graphs import Graph, WeightedGraph, dijkstra


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 4)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(1, 4)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(3, 4)
        self.graph.add_edge(3, 3)

        self.wg = WeightedGraph()
        self.wg.add_edge('A', 'B', 1)
        self.wg.add_edge('A', 'C', 2)
        self.wg.add_edge('B', 'D', 6)
        self.wg.add_edge('B', 'F', 2)
        self.wg.add_edge('C', 'E', 1)
        self.wg.add_edge('E', 'Q', 3)
        self.wg.add_edge('Q', 'S', 5)
        self.wg.add_edge('B', 'S', 1)
        self.wg.add_edge('E', 'F', 4)

    @given(st.integers(), st.integers())
    def test_add_remove_edge(self, e1, e2):
        self.graph.add_edge(e1, e2)
        before = copy.deepcopy(self.graph)
        self.graph.remove_edge(e1, e2)
        self.graph.add_edge(e1, e2)
        self.assertEqual(before, self.graph,
                         msg=f"\nbefore: {before} \nafter:{self.graph}")

    @given(st.integers(), st.integers())
    def test_add_edge_ints(self, e1, e2):
        self.graph.add_edge(e1, e2)
        self.assertTrue(self.graph.edge_in_graph((e1, e2)))

    @given(st.text(), st.text())
    def test_add_edge_text(self, e1, e2):
        self.graph.add_edge(e1, e2)
        self.assertTrue(self.graph.edge_in_graph((e1, e2)))

    def test_constructor(self):
        g2 = Graph(self.graph.edges())
        self.assertEqual(self.graph, g2)

    @given(st.integers(), st.integers())
    def test_remove_vertex(self, e1, e2):
        self.graph.add_edge(e1, e2)
        self.graph.remove_vertex(e1)
        self.assertNotIn(e1, self.graph.vertices())
        for vertex in self.graph.vertices():
            self.assertNotIn(e1, self.graph.neighbours(vertex))

    def test_dijk(self):

        paths = dijkstra(graph=self.wg, source='A',
                         cost=lambda u, v: self.wg.get_weight(u, v))
        shortest_path = dijkstra(
            graph=self.wg, source='A', target='Q', cost=lambda u, v: self.wg.get_weight(u, v))

        self.assertEqual(paths['A'], ['A'])
        self.assertEqual(paths['B'], ['A', 'B'])
        self.assertEqual(paths['C'], ['A', 'C'])
        self.assertEqual(paths['D'], ['A', 'B', 'D'])
        self.assertEqual(paths['E'], ['A', 'C', 'E'])
        self.assertEqual(paths['F'], ['A', 'B', 'F'])
        self.assertEqual(paths['Q'], ['A', 'C', 'E', 'Q'])
        self.assertEqual(paths['S'], ['A', 'B', 'S'])
        self.assertEqual(shortest_path['Q'], ['A', 'C', 'E', 'Q'])

    def test_edges_with_correspodning_vertices(self):
        for v, w in self.graph.edges():
            self.assertIn(v, self.graph.vertices())
            self.assertIn(w, self.graph.vertices())

    def test_shortest_path(self):
        source, target = 'A', 'Q'
        shortest_path1 = dijkstra(
            graph=self.wg, source=source, target=target, cost=lambda u, v: self.wg.get_weight(u, v))
        source, target = 'Q', 'A'
        shortest_path2 = dijkstra(
            graph=self.wg, source=source, target=target, cost=lambda u, v: self.wg.get_weight(u, v))
        self.assertEqual(shortest_path1['Q'], list(
            reversed(shortest_path2['A'])))


if __name__ == '__main__':
    unittest.main()
