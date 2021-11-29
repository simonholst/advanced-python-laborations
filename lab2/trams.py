from pprint import pprint

import graphs
import sys
import os
import json


class TramStop:

    def __init__(self, name, position=None, line_list=None) -> None:
        self.name = name
        self.position = position
        self.line_list = line_list

    def add_line(self, line):
        if not self.line_list:
            self.line_list = list()
        self.line_list.append(line)

    def __repr__(self):
        return f"TramStop: {self.name}"


class TramLine:

    def __init__(self, name, stop_list: list[TramStop]) -> None:
        self.name = name
        self.stop_list = stop_list

    def __repr__(self):
        return f"TramLine: {self.name}"


class TramNetwork(graphs.WeightedGraph):

    def __init__(self, edges=None):
        super().__init__(edges=edges)
        self.tram_stop_dict = dict()
        self.tram_line_dict = dict()
        # TODO ask Aarne why we can't access variable directly??
        self.weights = super().get_weights()
        self.vertices = super().vertices()
        self._edges = edges
        self.init()

    @property
    def edges(self):
        return self.edges()

    @edges.getter
    def edges(self):
        return super().edges()

    def init(self):
        sys.path.append('../lab1/')
        import tramdata as td
        if not os.path.exists(td.get_data_path(td.TRAMNETWORK)):
            td.create_network()
        with open(td.get_data_path(td.TRAMNETWORK), encoding='utf-8') as f:
            network = json.load(f)

        for stop in network['stops']:
            self.tram_stop_dict[stop] = TramStop(stop, network['stops'][stop], td.lines_via_stops(network['lines'], stop))

        for line in network['lines']:
            stop_list = list()
            for stop in network['lines'][line]:
                stop_list.append(self.tram_stop_dict[stop])
            self.tram_line_dict[line] = TramLine(line, stop_list)

        for stop in self.tram_stop_dict.values():
            self.add_vertex(stop)

        for stop, destinations in network['times'].items():
            for destination, weight in destinations.items():
                self.add_edge(stop, destination, weight)



    # @staticmethod
    # def init_tram_network():
    #     return network['stops'], network['lines'], network['times']


network = TramNetwork()
pprint(network.tram_stop_dict)

