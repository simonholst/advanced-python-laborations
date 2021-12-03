import graphviz
from graphs import dijkstra
import trams


def visualize(G, view='dot', name='mygraph', nodecolor=None):
    VG = graphviz.Graph('G', filename=name, engine=view, directory='graphs')
    for v in G.vertices:
        v = str(v)
        if v in nodecolor:
            VG.node(v, style='filled', fillcolor=nodecolor[v])
        else:
            VG.node(v)
    for v, w in G.edges:
        VG.edge(str(v), str(w))
    VG.render(format='png', view=True)


def view_shortest(G, source, target, cost=lambda u, v: 1):
    path = dijkstra(G, source, target, cost)[target]
    color_map = {str(v): 'orange' for v in path}
    visualize(G, view='neato', nodecolor=color_map)


def demo():
    G = trams.TramNetwork.read_tramnetwork()
    a, b = input('from,to ').split(',')
    a, b = G.tram_stop_dict[a], G.tram_stop_dict[b]
    view_shortest(G, a, b, cost=lambda u, v: G.get_weight(u, v))


if __name__ == '__main__':
    demo()


