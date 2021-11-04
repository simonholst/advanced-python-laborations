import json


def build_tram_stops(jsonobject):
    unparsed_tram_stops = json.load(jsonobject)
    stop_dictionary = dict()
    for stop in unparsed_tram_stops:
        stop_dictionary[stop] = {
            'lat': unparsed_tram_stops[stop]["position"][0],
            'lon': unparsed_tram_stops[stop]["position"][1]
        }
    print(stop_dictionary["Korsvägen"])
    return stop_dictionary


def build_tram_lines(lines):
    tram_lines = lines.read()
    tram_lines = tram_lines.split("\n\n")
    # TODO this could possibly delete the last line if file doesn't have empty space at the end
    if not tram_lines[-1]:
        del tram_lines[-1]

    line_dict = dict()
    for line in tram_lines:
        line = line.strip()  # Removes any leading spaces, see line 10 in tramlines.txt
        # TODO line below only works for lines with one digit (0-9) need to handle bigger numbers as well
        line_dict[line[0]] = return_stops_for_line(line)

    print(line_dict["1"])


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
