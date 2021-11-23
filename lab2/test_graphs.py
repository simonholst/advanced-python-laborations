import copy
import unittest
from hypothesis import given, strategies as st

from lab2.graphs import Graph


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
        print(self.graph)

    @given(st.integers(), st.integers())
    def test_add_remove_edge(self, e1, e2):
        self.graph.add_edge(e1, e2)
        before = copy.deepcopy(self.graph)
        self.graph.remove_edge(e1, e2)
        self.graph.add_edge(e1, e2)
        self.assertEqual(before, self.graph, msg=f"\nbefore: {before} \nafter:{self.graph}")

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
            self.assertNotIn(e1, self.graph.get_vertex_value(vertex))

    def test_dijk(self):
        self.graph.dijkstra(0, cost=lambda u, v: u*v)


if __name__ == '__main__':
    unittest.main()