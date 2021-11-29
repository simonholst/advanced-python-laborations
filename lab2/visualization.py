import graphviz
from graphs import Graph, dijkstra


def visualize(G, view, nodecolor):
    pass


def view_shortest(G, source, target, cost=lambda u, v: 1):
    path = dijkstra(G, source, target, cost)
    print(path)
    color_map = {str(v): 'orange' for v in path}
    print(color_map)
    visualize(G, view='view', nodecolor=color_map)


def demo():
    G = Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (3, 6), (3, 7), (6, 7)])
    VG = graphviz.Graph('G', filename='process.gv', engine='sfdp')
    for v in G.vertices():
        VG.node(str(v))
    for v, w in G.edges():
        VG.edge(str(v), str(w))
    view_shortest(G, 2, 6)
    VG.save()
    VG.render(format='png').replace('\\', '/')


if __name__ == '__main__':
    demo()
