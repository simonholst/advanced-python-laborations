import random
import unittest
from trams import TramNetwork
import sys
from hypothesis import given, strategies as st
from collections import deque


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.network = TramNetwork.read_tramnetwork()

    def test_stops_exist(self):
        stopset = {
            stop for line in self.network.tram_line_dict for stop in self.network.tram_line_dict[line]}
        stops = [stop for stop in self.network.tram_stop_dict]
        for stop in stopset:
            self.assertIn(stop.name, stops, msg=f'{stop.name} not in stop dict')

    def test_lines_correct_group(self):
        sys.path.append('../lab1/')
        import tramdata as td
        with open(td.get_data_path(td.TRAMLINES), 'r', encoding='utf-8') as f:
            text_lines = f.read()
            text_lines = text_lines.split("\n\n")
            i = 0
            for line in self.network.tram_line_dict:
                current = text_lines[i].split("\n")
                del current[0]
                for stop in self.network.tram_line_dict[line]:
                    self.assertIn(
                        stop.name, current[0].lower(), msg=stop.name + 'not in tramlines.txt on line ' + str(current[0]))
                    del current[0]
                self.assertTrue(len(current) == 0)
                i += 1

    @given(st.text(), st.text())
    def test_add(self, e1, e2):
        self.network.add_edge(e1, e2)
        self.assertTrue(self.network.edge_in_graph((e1, e2)))

    def test_connectedness(self):
        def BFS(G, node, goal=lambda n: False):
            Q = deque()
            explored = [node]
            Q.append(node)
            while Q:
                v = Q.popleft()
                if goal(v):
                    return v
                for w in G.neighbours(v):
                    if w not in explored:
                        explored.append(w)
                        Q.append(w)
            return explored

        for stop in list(self.network.tram_stop_dict):
            self.assertEqual(len(BFS(self.network, self.network.tram_stop_dict[stop])),
                             len(self.network.tram_stop_dict))

    def test_vertices(self):
        self.assertEqual(len(self.network.vertices), len(self.network.tram_stop_dict))


