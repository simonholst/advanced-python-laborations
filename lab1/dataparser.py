import json


def build_tram_stops(json_object):
    stops = json.load(json_object)
    return {stop: {'lat': stops[stop]["position"][0], 'lon': stops[stop]["position"][1]} for stop in stops}


def build_tram_lines(tram_lines):
    return {find_line_number(line.strip()): create_stops_for_line(line) for line in tram_lines}


def build_tram_lines_and_times(lines):
    tram_lines = lines.read()
    tram_lines = tram_lines.split("\n\n")
    if not tram_lines[-1]:
        del tram_lines[-1]
    return build_tram_lines(tram_lines), build_tram_times(tram_lines)


def build_tram_times(tram_lines):
    stop_time_dict = dict()
    for line in tram_lines:
        stations = line.split("\n")
        # remove first element, since it is the key value for the line
        del stations[0]
        one_line_time_dict = dict()
        prev_station = None
        prev_time = None
        for station in stations:
            elements = str(station).split("  ")
            # Removes every element which is an empty string, preserving only station and time
            station_name, station_time = list(filter(lambda a: a != '', elements))
            station_time = station_time.strip()
            if prev_station:
                one_line_time_dict[prev_station] = {station_name: calc_diff_in_time(station_time, prev_time)}

            prev_station = station_name
            prev_time = station_time
        stop_time_dict.update(one_line_time_dict)

    return stop_time_dict


def find_line_number(line: str):
    line_number = ''
    i = 0
    while True:
        if line[i] == ':':
            return line_number
        line_number += line[i]
        i += 1


def stops_for_line(line):
    stations = line.split("\n")
    # remove first element, since it is the key value for the line
    del stations[0]
    stops = []
    for station in stations:
        elements = str(station).split("  ")
        # Removes every element which is an empty string, preserving only station and time
        elements = list(filter(lambda a: a != '', elements))
        stops.append(elements[0])

    return stops


def create_stops_for_line(line):
    stations = line.split("\n")
    # remove first element, since it is the key value for the line
    del stations[0]
    stops = []
    for station in stations:
        elements = str(station).split("  ")
        station_name = elements[0]
        stops.append(station_name)

    return stops


def calc_diff_in_time(now, previous):
    mins100, mins = now.split(":")
    prev_mins100, prev_mins = previous.split(":")
    return (int(mins100) - int(prev_mins100)) * 100 + (int(mins) - int(prev_mins))






def create_tram_stops():
    apply_func_to_file(build_tram_stops, "data/tramstops.json")


def create_tram_lines():
    print(apply_func_to_file(build_tram_lines, 'data/tramlines.txt'))

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

def create_tram_lines_and_times():
    apply_func_to_file(build_tram_lines_and_times, "data/tramlines.txt")


def apply_func_to_file(func, path):
    try:
        with open(path, 'r') as file:
            return func(file)
    except FileNotFoundError:
        with open('../' + path, 'r') as file:
            return func(file)


create_tram_lines_and_times()

#create_tram_stops()
#create_tram_lines()
