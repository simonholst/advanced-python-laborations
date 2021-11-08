import json
import re


def build_tram_stops(json_object):
    stops = json.load(json_object)
    return {stop: {'lat': stops[stop]["position"][0], 'lon': stops[stop]["position"][1]} for stop in stops}


def build_tram_lines(tram_lines):
    return {find_line_number(line): create_stops_for_line(line) for line in tram_lines}


def build_tram_lines_and_times(lines):
    tram_lines = lines.read()
    tram_lines = tram_lines.split("\n\n")
    if not tram_lines[-1]:
        del tram_lines[-1]
    return build_tram_lines(tram_lines), build_tram_times(tram_lines)


def find_line_number(line: str):
    # TODO regex ^\d+:
    line.strip()
    line_number = ''
    i = 0
    while True:
        if line[i] == ':':
            return line_number
        if line[i].isdigit():
            line_number += line[i]
        i += 1


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
    # TODO make cleaner
    mins100, mins = now.split(":")
    prev_mins100, prev_mins = previous.split(":")
    return (int(mins100) - int(prev_mins100)) * 100 + (int(mins) - int(prev_mins))


def create_tram_stops():
    return apply_func_to_file(build_tram_stops, "data/tramstops.json")


def create_tram_lines_and_times():
    return apply_func_to_file(build_tram_lines_and_times, "data/tramlines.txt")


def apply_func_to_file(func, path):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            return func(file)
    except FileNotFoundError:
        with open('../' + path, 'r', encoding="utf-8") as file:
            return func(file)


def stations_and_times_list(expr):
    pattern = re.compile(r"((?:[a-öA-Ö]+ ?)+\S) *(\d\d:\d\d)", flags=re.IGNORECASE)  # flag = case insensitive
    return pattern.findall(expr)


def build_tram_times(tram_lines):
    # FIXME maybe change to using dict() operation on the list of tuples
    stop_time_dict = dict()
    for line in tram_lines:
        station_time_tuples = stations_and_times_list(line)
        for i in range(len(station_time_tuples) - 1):
            station = station_time_tuples[i][0]
            next_station = station_time_tuples[i+1][0]
            value = calc_diff_in_time(station_time_tuples[i+1][1], station_time_tuples[i][1])
            if station not in stop_time_dict:
                stop_time_dict[station] = {next_station: value}
            else:
                stop_time_dict[station].update({next_station: value})

    return stop_time_dict


def main():
    stops = create_tram_stops()
    lines, times = create_tram_lines_and_times()


if __name__ == "__main__":
    main()


