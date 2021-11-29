import graphviz
from graphs import Graph, dijkstra


def visualize(G, view='dot', name='mygraph', nodecolor=None):
    VG = graphviz.Graph('G', filename=name, engine=view, directory='graphs')
    for v in G.vertices():
        v = str(v)
        if v in nodecolor:
            VG.node(v, style='filled', fillcolor=nodecolor[v])
        else:
            VG.node(v)
    for v, w in G.edges():
        VG.edge(str(v), str(w))
    VG.render(format='png', view=True)


def view_shortest(G, source, target, cost=lambda u, v: 1):
    path = dijkstra(G, source, target, cost)[target]
    print(path)
    color_map = {str(v): 'orange' for v in path}
    print(color_map)
    visualize(G, view='sfdp', nodecolor=color_map)


def demo():
    G = Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (3, 6), (3, 7), (6, 7)])
    view_shortest(G, 2, 6)


if __name__ == '__main__':
    demo()
