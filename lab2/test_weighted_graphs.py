import unittest

from graphs import WeightedGraph


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.graph = WeightedGraph()
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 4)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(1, 4)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(3, 4)
        self.graph.add_edge(3, 3)
        self.graph.add_edge(5, 7, 2)

    def test_something(self):
        self.graph.set_weight(0, 1, 8)
        print(self.graph.get_weight(0, 1))
        print(self.graph.get_weight(1, 0))


if __name__ == '__main__':
    unittest.main()
