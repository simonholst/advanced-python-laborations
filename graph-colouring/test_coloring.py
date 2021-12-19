import unittest
import lab2.graphs as gr
import random
import coloring


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.colors = {'red', 'green', 'blue'}
        self.G = self.create_graph(10, 3)

    def create_graph(self, n_nodes, n_colors):
        nodes = [i for i in range(n_nodes)]
        max_n_edges = len(self.colors) - 1

        graph = gr.Graph()
        for node in nodes:
            graph.add_vertex(node)

        for node in graph.vertices:
            attempts = 0
            while len(graph.neighbours(node)) < max_n_edges and attempts < 1000:
                rand_node = random.randint(0, len(nodes) - 1)
                if rand_node != node and len(graph.neighbours(rand_node)) < max_n_edges:
                    graph.add_edge(node, list(graph.vertices)[rand_node])
                attempts += 1
        return graph

    def test_1(self):
        print(self.G.edges)
        coloring.viz_color_graph(self.G, self.colors)

