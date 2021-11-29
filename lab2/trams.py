
import tramdata as td
import graphs
import sys
import os
sys.path.append('../lab1/')


class TramStop():

    def __init__(self, name, position=None, line_list=None) -> None:
        self.name = name
        self.position = position
        self.line_list = line_list

    def add_line(self, line):
        if not self.line_list:
            self.line_list = list()
        self.line_list.append(line)


class TramLine():

    def __init__(self, name, stop_list: list(TramStop)) -> None:
        self.name = name
        self.stop_list = stop_list


class TramNetwork(graphs.WeightedGraph):

    def __init__(self, edges=None):
        super().__init__(edges=edges)
        tramstop_dict = dict()
        tramline_dict = dict()
        vertices = super().vertices()
        edges = super().edges()
        weights = super()._weights()

    @staticmethod
    def init_tramstop():
        td.create_network()


print(os.path.exists('data/tramnetwork.json'))
