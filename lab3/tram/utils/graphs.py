import math
from collections import defaultdict


class Graph:

    def __init__(self, edges=None):
        self._adj_list = {}
        self._vertex_values = {}
        if edges is not None:
            for edge in edges:
                self.add_edge(edge[0], edge[1])

    def add_edge(self, a, b):
        self.add_vertex(a)
        self._adj_list[a].add(b)
        self.add_vertex(b)
        self._adj_list[b].add(a)

    @property
    def vertices(self):
        return self._adj_list.keys()

    @property
    def edges(self):
        eds = []
        for a in self._adj_list:
            for b in self._adj_list[a]:
                # Only add in one direction to avoid duplicates
                if a <= b:
                    eds.append((a, b))
        return eds

    def add_vertex(self, vertex):
        if vertex not in self._adj_list:
            self._adj_list[vertex] = set()

    def remove_vertex(self, vertex):
        if vertex in self._adj_list:
            for v in self._adj_list[vertex]:
                # Avoid changing set during removal since loops are allowed, vertex is popped after
                if v != vertex:
                    self._adj_list[v].remove(vertex)
            self._adj_list.pop(vertex)

    def remove_edge(self, vertex1, vertex2):
        if vertex2 in self._adj_list[vertex1]:
            self._adj_list[vertex1].remove(vertex2)

        if vertex1 in self._adj_list[vertex2]:
            self._adj_list[vertex2].remove(vertex1)

    def get_vertex_value(self, vertex):
        return self._vertex_values.get(vertex, None)

    def set_vertex_value(self, vertex, value):
        self._vertex_values[vertex] = value

    def edge_in_graph(self, edge):
        if not (edge[0] in self._adj_list and edge[1] in self._adj_list[edge[0]]):
            return False
        if not (edge[1] in self._adj_list and edge[0] in self._adj_list[edge[1]]):
            return False
        return True

    def neighbours(self, vertex):
        return self._adj_list.get(vertex, None)

    def __len__(self):
        return len(self.vertices)

    def __str__(self):
        return str(self._adj_list)

    def __getitem__(self, v):
        return self._adj_list[v]

    def __eq__(self, other):
        return self._adj_list == other._adj_list


class WeightedGraph(Graph):

    def __init__(self, edges=None):
        super().__init__(edges)
        self._weights = dict()

    @property
    def weights(self):
        return self._weights

    def get_weight(self, vertex1, vertex2):
        try:
            return self._weights[vertex1][vertex2]
        except KeyError:
            try:
                return self._weights[vertex2][vertex1]
            except KeyError:
                return None

    def set_weight(self, vertex1, vertex2, weight):
        if vertex1 not in self._weights:
            self._weights[vertex1] = dict()
        self._weights[vertex1][vertex2] = weight

    def add_edge(self, a, b, weight=None):
        super().add_edge(a, b)
        self.set_weight(a, b, weight)


def dijkstra(graph, source, target=None, cost=lambda u, v: 1):
    Q = set()
    dist = dict()
    prev = dict()

    for v in graph.vertices:
        dist[v] = math.inf
        prev[v] = None
        Q.add(v)
    dist[source] = 0

    while Q:
        u = min(Q, key=lambda x: dist[x])

        Q.remove(u)

        if target and u == target:
            return make_path_dict({u: dist[u]}, prev)

        for v in [nbr for nbr in graph.neighbours(u) if nbr in Q]:
            alt = dist[u] + cost(u, v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return make_path_dict(dist, prev)


def dijkstra_with_lines(graph, source, target, cost=lambda u, v: 1, transition_cost=0):
    Q = set()
    dist = dict()
    prev = dict()

    for v in graph.vertices:
        dist[v] = math.inf
        prev[v] = None
        Q.add(v)

    dist[source] = 0

    while Q:
        u = min(Q, key=lambda x: dist[x])

        Q.remove(u)

        if u == target:
            return make_path_dict({u: dist[u]}, prev), dist[u]

        for v in [nbr for nbr in graph.neighbours(u) if nbr in Q]:
            change_cost = 0
            if u[1] != v[1]:
                change_cost = transition_cost

            alt = dist[u] + cost(u, v) + change_cost
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    raise NotImplemented


def make_path_dict(dist, prev):
    res = defaultdict(list)
    for key, value in dist.items():
        if value == math.inf:
            continue
        k = key
        while prev[k]:
            res[key].append(prev[k])
            k = prev[k]
        res[key].reverse()
        res[key].append(key)
    return dict(res)

# dijkstra(g, g[1], cost=lambda u, v: g.get_weight(u, v))
