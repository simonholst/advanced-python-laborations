import copy
import pprint
from collections import deque
import lab2.graphs as gr
import graphviz


def simplify(graph, n=4):
    graph = copy.deepcopy(graph)
    dq = deque()
    while len(graph.vertices):
        for vertex in graph.vertices:
            if len(graph.neighbours(vertex)) < n:
                dq.appendleft(vertex)
                graph.remove_vertex(vertex)
                break
    return dq


def rebuild(graph, stack, colors):
    color_dict = {}
    for vertex in stack:
        used_colors = set()
        for neighbour in graph.neighbours(vertex):
            if neighbour in color_dict:
                used_colors.add(color_dict[neighbour])
        color_dict[vertex] = colors.difference(used_colors).pop()
    return color_dict


def viz_color_graph(graph, colors):
    stack = simplify(graph, len(colors))
    color_dict = rebuild(graph, stack, colors)
    VG = graphviz.Graph('G', filename='my-color-graph', engine='dot', directory='graphs')
    for v in graph.vertices:
        VG.node(str(v), style='filled', fillcolor=color_dict[v])
    for v, w in graph.edges:
        VG.edge(str(v), str(w))
    VG.render(format='svg', view=True)


def demo():
    colors = {'red', 'green', 'blue'}
    G = gr.Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (3, 6), (3, 7), (6, 7)])
    viz_color_graph(G, colors)


if __name__ == '__main__':
    demo()
