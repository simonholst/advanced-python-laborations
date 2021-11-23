class Graph:

    def __init__(self):
        self._adj_list = {}

    def add_edge(self, a, b):
        if a not in self._adj_list:
            self._adj_list[a] = set()
        self._adj_list[a].add(b)

        if b not in self._adj_list:
            self._adj_list[b] = set()
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

    def __str__(self):
        return str(self._adj_list)

    def __getitem__(self, v):
        return self._adj_list[v]


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

