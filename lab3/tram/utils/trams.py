import math
import pprint
from math import pi, sqrt, cos
from .graphs import WeightedGraph, dijkstra, dijkstra_with_lines
import sys
import os
import json
import logging
logger = logging.getLogger('tramlogger')


class TramStop:

    def __init__(self, name, position=None, line_list=None) -> None:
        self._name = name
        self._position = TramStop.__convert_position_to_float(position)
        self._line_list = line_list

    @staticmethod
    def __convert_position_to_float(position):
        return {'lat': float(position['lat']), 'lon': float(position['lon'])}

    def add_line(self, line):
        if not self.line_list:
            self.line_list = list()
        self.line_list.append(line)

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if type(value) != dict:
            raise TypeError('Position has to a dict')
        self._position = value

    def set_position(self, lat, lon):
        self._position = {'lat': lat, 'lon': lon}

    @property
    def line_list(self):
        return self._line_list

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    def __le__(self, other):
        try:
            return self._name < other.name
        except AttributeError:
            return other.__le__(self.name)

    def __eq__(self, other):
        try:
            return self._name == other.name
        except AttributeError:
            return other.__eq__(self.name)

    @line_list.setter
    def line_list(self, value):
        self._line_list = value


class TramLine:

    def __init__(self, number, stop_list: list[TramStop]) -> None:
        self._number = number
        self._stop_list = stop_list

    @property
    def number(self):
        return self._number

    @property
    def stop_list(self):
        return self._stop_list

    def __repr__(self):
        return self._number

    def __str__(self):
        return self._number

    def __hash__(self):
        return hash(self._number)

    def __iter__(self):
        return iter(self._stop_list)


class TramNetwork(WeightedGraph):

    TRAM_FILE = 'tramnetwork.json'

    def __init__(self, tramfile, edges=None):
        super().__init__(edges=edges)
        self.tram_stop_dict = dict()
        self.tram_line_dict = dict()
        self.__init_network(tramfile)

    def __len__(self):
        return len(self.tram_stop_dict)

    def __init_network(self, tram_file):
        sys.path.append('../lab1/')
        import tramdata as td
        network = TramNetwork.__load_file(tram_file, td)
        self.__add_tram_stops(network, td)
        self.__add_tram_lines(network)
        self.__add_vertices()
        self.__add_edges(network)

    @staticmethod
    def __load_file(tram_file, td):
        if not os.path.exists(td.get_data_path(tram_file)):
            td.create_network()
        with open(td.get_data_path(tram_file), encoding='utf-8') as f:
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
            for line in stop.line_list:
                self.add_vertex((stop, line))

    def __add_edges(self, network):
        for stop, destinations in network['times'].items():
            stop = self.tram_stop_dict[stop]
            for line in stop.line_list:
                destinations = [self.tram_stop_dict[d] for d in destinations]
                for destination in destinations:
                    if line in destination.line_list:
                        self.add_edge((stop, line), (destination, line), weight=network['times'][stop.name][destination.name])
                for otherline in stop.line_list:
                    if line != otherline:
                        self.add_edge((stop, line), (stop, otherline), weight=0)

    def all_lines(self) -> list:
        return list(self.tram_line_dict.values())

    def all_stops(self) -> list:
        return list(self.tram_stop_dict.values())

    @staticmethod
    def geo_distance(a, b):
        R = 6371.009

        d_lat = abs(float(a.position['lat']) -
                    float(b.position['lat'])) * (pi / 180)
        lat_m = ((float(a.position['lat']) +
                  float(b.position['lat'])) / 2) * (pi / 180)
        d_lon = abs(float(a.position['lon']) -
                    float(b.position['lon'])) * (pi / 180)

        return round(R * sqrt((d_lat ** 2) + (cos(lat_m) * d_lon) ** 2), 3)

    def line_stops(self, line):
        if type(line) == str:
            return self.tram_line_dict.get(line, None).stop_list
        else:
            return line.stop_list

    def remove_lines(self, lines: list[str]):
        for line in lines:
            del self.tram_line_dict[line]

    def stop_lines(self, a):
        return self.tram_stop_dict[a].line_list

    def stop_position(self, a):
        if type(a) == str:
            return self.tram_stop_dict[a].position['lat'], self.tram_stop_dict[a].position['lon']
        else:
            return a.position['lat'], a.position['lon']

    def transition(self, a, b, cost=lambda u, v: 1, transition_cost=0):
        paths = []
        a = self.tram_stop_dict[a]
        b = self.tram_stop_dict[b]
        for source in [v for v in self.vertices if v[0] == a]:
            for target in [v for v in self.vertices if v[0] == b]:
                path, time = dijkstra_with_lines(self, source, target, cost=cost,
                                                 transition_cost=transition_cost)
                paths.append((path, time))

        shortest = min(paths, key=lambda x: x[1])
        return shortest

    def extreme_positions(self):
        stops = self.tram_stop_dict.values()
        min_lon = min([stop.position['lon'] for stop in stops])
        min_lat = min([stop.position['lat'] for stop in stops])
        max_lon = max([stop.position['lon'] for stop in stops])
        max_lat = max([stop.position['lat'] for stop in stops])
        return min_lon, min_lat, max_lon, max_lat

    @classmethod
    def read_tram_network(cls, tram_file=TRAM_FILE):
        return cls(tram_file)