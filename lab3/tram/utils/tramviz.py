from .trams import TramNetwork
from .graphs import dijkstra
import graphviz
import json
import os
from django.conf import settings

# to be defined in Bonus task 1, but already included as mock-up
# from .trams import specialize_stops_to_lines, specialized_geo_distance, specialized_transition_time

SHORTEST_PATH_SVG = os.path.join(settings.BASE_DIR,
                                 'tram/templates/tram/images/shortest_path.svg')

# assign colors to lines, indexed by line number; not quite accurate
gbg_linecolors = {
    1: 'gray', 2: 'yellow', 3: 'blue', 4: 'green', 5: 'red',
    6: 'orange', 7: 'brown', 8: 'purple', 9: 'blue',
    10: 'lightgreen', 11: 'black', 13: 'pink'}


def scaled_position(network):
    # compute the scale of the map
    min_lat, min_lon, max_lat, max_lon = network.extreme_positions()
    size_x = max_lon - min_lon
    scale_factor = len(network) / 4  # heuristic
    x_factor = scale_factor / size_x
    size_y = max_lat - min_lat
    y_factor = scale_factor / size_y

    return lambda xy: (x_factor * (xy[0] - min_lon), y_factor * (xy[1] - min_lat))


# Bonus task 2: redefine this so that it returns the actual traffic information
import urllib.parse


def stop_url(stop):
    google_url = 'https://www.google.com/search'
    attrs = urllib.parse.urlencode({'q': f'Gothenburg {stop}'})
    return f'{google_url}?{attrs}'


# You don't probably need to change this

def network_graphviz(network, outfile, colors=None, positions=scaled_position):
    dot = graphviz.Graph(engine='fdp', graph_attr={'size': '12,12'})

    for stop in network.all_stops():
        stop = stop.name
        x, y = network.stop_position(stop)
        if positions:
            x, y = positions(network)((x, y))
        pos_x, pos_y = str(x), str(y)

        if colors:
            col = colors(stop)  # set this to white to create gbg_tramnet.svg
        else:
            col = 'white'

        dot.node(str(stop), label=f'{stop}', shape='rectangle', pos=f"{pos_x},{pos_y}!",
                 fontsize='8pt', width='0.4', height='0.05',
                 URL=stop_url(stop),
                 fillcolor=col, style='filled')

    for line in network.all_lines():
        line = line.number
        stops = network.line_stops(line)
        for i in range(len(stops) - 1):
            dot.edge(stops[i].name, stops[i + 1].name,
                     color=gbg_linecolors[int(line)], penwidth=str(2))

    dot.format = 'svg'
    s = dot.pipe().decode('utf-8')
    with open(outfile, 'w') as file:
        file.write(s)


def show_shortest(dep, dest):
    network = TramNetwork.read_tram_network()
    time_path = network.transition_time(dep, dest)
    geo_path = network.transition_distance(dep, dest)
    network_graphviz(network, SHORTEST_PATH_SVG)
    return time_path, geo_path
