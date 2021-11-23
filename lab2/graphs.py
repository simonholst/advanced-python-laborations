class Graph:

    def __init__(self, edges=None):
        self._adj_list = {}
        if edges is not None:
            for edge in edges:
                self.add_edge(edge[0], edge[1])

    def add_edge(self, a, b):
        self.add_vertex(a)
        self._adj_list[a].add(b)
        self.add_vertex(b)
        self._adj_list[b].add(a)

    def vertices(self):
        return self._adj_list.keys()

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
        return self._adj_list.get(vertex, None)

    def set_vertex_value(self, vertex, value):
        self._adj_list[vertex] = value

    def edge_in_graph(self, edge):
        if not (edge[0] in self._adj_list and edge[1] in self._adj_list[edge[0]]):
            return False
        if not (edge[1] in self._adj_list and edge[0] in self._adj_list[edge[1]]):
            return False
        return True

    # TODO cost??
    def dijkstra(self, source, cost=lambda u, v: 1):
        print(cost(2, 3))
        pass

    # TODO neighbors method???

    def __len__(self):
        return len(self.vertices())

    def __str__(self):
        return str(self._adj_list)

    def __getitem__(self, v):
        return self._adj_list[v]

    def __eq__(self, other):
        # TODO ask how to do this without accessing private variable.
        # Possibly deepcopy getter
        return self._adj_list == other._adj_list


class WeightedGraph(Graph):

    def __init__(self, edges=None):
        super().__init__(edges)
        self._weights = dict()

    def get_weight(self, vertex1, vertex2):
        # TODO make nicer? Ask TA?
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

    # TODO ask if we need these? Feels reasonable? Weights directly in graph? Redundant?
    #########################################################################
    def add_edge(self, a, b, weight=None):
        super().add_edge(a, b)
        self.set_weight(a, b, weight)

    def remove_edge(self, vertex1, vertex2):
        pass

class ValueGraph(Graph):
    """
    Graph where vertices have values
    """
    def __init__(self):
        super().__init__()
        self._value_list = {}

    def get_value(self, v):
        return self._value_list.get(v, None)

    def set_value(self, v, x):
        """Destructive update of value"""
        self._value_list[v] = x


class Tree(Graph):
    """Trees as graphs with certain restrictions"""
    def __init__(self, root):
        super().__init__()
        self._adj_list = {root: set()}

    def add_edge(self, a, b):
        if a not in self._adj_list:
            print("Parent does not exist:", a)
        elif b in self._adj_list:
            print("Child already exists:", b)
        else:
            self._adj_list[a].add(b)
            self._adj_list[b] = set()