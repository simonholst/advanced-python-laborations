import json


def build_tram_stops(jsonobject):
    unparsed_tram_stops = json.load(jsonobject)
    stop_dictionary = dict()
    for stop in unparsed_tram_stops:
        stop_dictionary[stop] = {
            'lat': unparsed_tram_stops[stop]["position"][0],
            'lon': unparsed_tram_stops[stop]["position"][1]
        }
    return stop_dictionary


def build_tram_lines(lines):
    tram_lines = lines.read()
    tram_lines = tram_lines.split("\n\n")
    del tram_lines[-1]  # TODO this could possibly delete the last line if file doesn't have empty space at the end 

    line_dict = dict()
    for line in tram_lines:
        line = line.strip() # Removes any leading spaces, see line 10 in tramlines.txt
        # TODO line below only works for lines with one digit (0-9) need to handle bigger numbers as well
        line_dict[line[0]] = return_stops_for_line(line)

    # print(line_dict["13"])


def return_stops_for_line(line):
    stations = line.split("\n")
    # remove first element, since it is the key value for the line
    del stations[0]
    stops = []
    for station in stations:
        elements = str(station).split("  ")
        stops.append(elements[0])

    return stops


# Temporary solution, since PyCharm file system is a struggle
def create_tram_stops():
    with open("tramstops.json", 'r') as file:
        build_tram_stops(file)
    # try:
    #     with open("data/tramstops.json", 'r') as file:
    #         build_tram_stops(file)
    # except FileNotFoundError:
    #     with open("C:/Users/Milvi/PycharmProjects/laboration-1/data/tramstops.json", 'r') as file:
    #         build_tram_stops(file)


def create_tram_lines():
    with open("tramlines.txt", 'r') as file:
        build_tram_lines(file)
    # try:
    #     with open("data/tramlines.txt", 'r') as file:
    #         build_tram_lines(file)
    # except FileNotFoundError:
    #     with open("C:/Users/Milvi/PycharmProjects/laboration-1/data/tramlines.txt", 'r') as file:
    #         build_tram_lines(file)

create_tram_lines()
