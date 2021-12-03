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
        return self.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __le__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name


class TramLine:

    def __init__(self, name, stop_list: list[TramStop]) -> None:
        self.name = name
        self.stop_list = stop_list

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __iter__(self):
        return iter(self.stop_list)


class TramNetwork(graphs.WeightedGraph):

    TRAM_FILE = 'tramnetwork.json'

    def __init__(self, tramfile, edges=None):
        super().__init__(edges=edges)
        self.tram_stop_dict = dict()
        self.tram_line_dict = dict()
        self.init_network(tramfile)

    def __len__(self):
        return len(self.tram_stop_dict)

    def init_network(self, tramfile):
        sys.path.append('../lab1/')
        import tramdata as td
        network = TramNetwork.__load_file(tramfile, td)
        self.__add_tram_stops(network, td)
        self.__add_tram_lines(network)
        self.__add_vertices()
        self.__add_edges(network)

    @staticmethod
    def __load_file(tramfile, td):
        if not os.path.exists(td.get_data_path(tramfile)):
            td.create_network()
        with open(td.get_data_path(tramfile), encoding='utf-8') as f:
            network = json.load(f)
        return network

    def __add_tram_stops(self, network, td):
        for stop in network['stops']:
            self.tram_stop_dict[stop] = TramStop(stop, network['stops'][stop],
                                                 td.lines_via_stops(network['lines'], stop))

    def __add_tram_lines(self, network):
        for line in network['lines']:
            stop_list = list()
            for stop in network['lines'][line]:
                stop_list.append(self.tram_stop_dict[stop])
            self.tram_line_dict[line] = TramLine(line, stop_list)

    def __add_vertices(self):
        for stop in self.tram_stop_dict.values():
            self.add_vertex(stop)

    def __add_edges(self, network):
        for stop, destinations in network['times'].items():
            stop = self.tram_stop_dict[stop]
            destinations = [self.tram_stop_dict[d] for d in destinations]
            for destination in destinations:
                self.add_edge(stop, destination, network['times'][stop.name][destination.name])

    @classmethod
    def read_tramnetwork(cls, tramfile=TRAM_FILE):
        return cls(tramfile)

