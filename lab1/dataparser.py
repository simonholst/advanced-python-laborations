import json


def build_tram_stops(jsonobject):
    stops = json.load(jsonobject)
    return {stop: {'lat': stops[stop]["position"][0], 'lon': stops[stop]["position"][1]} for stop in stops}



def build_tram_lines(lines):
    tram_lines = lines.read()
    tram_lines = tram_lines.split("\n\n")
    if not tram_lines[-1]:
        del tram_lines[-1]

    line_dict = dict()
    for line in tram_lines:
        line = line.strip()  # Removes any leading spaces, see line 10 in tramlines.txt
        line_dict[find_line_number(line)] = return_stops_for_line(line)

    print(line_dict.keys())


def find_line_number(line: str):
    line_number = ''
    i = 0
    while True:
        if line[i] == ':':
            return line_number
        line_number += line[i]
        i += 1


def return_stops_for_line(line):
    stations = line.split("\n")
    # remove first element, since it is the key value for the line
    del stations[0]
    stops = []
    for station in stations:
        elements = str(station).split("  ")
        stops.append(elements[0])

    return stops


def create_tram_stops():
    apply_func_to_file(build_tram_stops, "data/tramstops.json")


def create_tram_lines():
    apply_func_to_file(build_tram_lines, 'data/tramlines.txt')

    # path = os.getcwd()
    # paths = path.split("\\")
    # if len(paths) < 1:
    #     paths = path.split("/")
    #
    # if "lab1" in path:
    #     paths.pop(-1)
    #
    # paths.append('data')
    # paths.append('tramlines.txt')
    # path = '/'.join(paths)
    #
    # with open(path, 'r') as file:
    #     build_tram_lines(file)


def apply_func_to_file(func, path):
    try:
        with open(path, 'r') as file:
            func(file)
    except FileNotFoundError:
        with open('../' + path, 'r') as file:
            func(file)


create_tram_stops()
create_tram_lines()
