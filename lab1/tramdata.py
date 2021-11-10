import json
import os
import re
import sys
from lab1.invalidcommandexception import InvalidCommandException
from math import pi, sqrt, cos
from typing import List, Tuple
from invalidcommandexception import InvalidCommandException

TRAMLINES = 'tramlines.txt'
TRAMSTOPS = 'tramstops.json'
TRAMNETWORK = 'tramnetwork.json'


def build_tram_stops(json_object) -> dict:
    stops = json.load(json_object)
    return {stop: {'lat': stops[stop]["position"][0], 'lon': stops[stop]["position"][1]} for stop in stops}


def build_tram_lines(tram_lines: List[str]) -> dict:
    return {find_line_number(line): create_stops_for_line(line) for line in tram_lines}


def build_tram_lines_and_times(text_file) -> Tuple[dict, dict]:
    tram_lines = text_file.read()
    tram_lines = tram_lines.split("\n\n")
    if not tram_lines[-1]:
        del tram_lines[-1]
    return build_tram_lines(tram_lines), build_tram_times(tram_lines)


def find_line_number(line: str) -> str:
    return re.compile(r" *(\d+):\s").search(line).groups()[0]


def create_stops_for_line(line: str) -> List[str]:
    return re.compile(r"(?:[a-ö]+ ?)+\S", flags=re.IGNORECASE).findall(line)


def calc_diff_in_time(now: str, previous: str) -> int:
    # TODO make cleaner
    mins100, mins = now.split(":")
    prev_mins100, prev_mins = previous.split(":")
    return (int(mins100) - int(prev_mins100)) * 100 + (int(mins) - int(prev_mins))


def create_tram_stops(file_path: str) -> dict:
    with open(get_data_path(TRAMSTOPS), 'r', encoding='utf-8') as f:
        return build_tram_stops(f)


def create_tram_lines_and_times(file_path: str):
    with open(get_data_path(TRAMLINES), 'r', encoding='utf-8') as f:
        return build_tram_lines_and_times(f)


def apply_func_to_file(func, path: str):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            return func(file)
    except FileNotFoundError:
        with open('../' + path, 'r', encoding="utf-8") as file:
            return func(file)


def stations_and_times_list(expr: str) -> List[tuple]:
    return re.compile(r"((?:[a-ö]+ ?)+\S) *(\d\d:\d\d)", flags=re.IGNORECASE).findall(expr)


def build_tram_times(tram_lines: List[str]) -> dict:
    # FIXME maybe change to using dict() operation on the list of tuples
    stop_time_dict = dict()
    for line in tram_lines:
        station_time_tuples = stations_and_times_list(line)
        for i in range(len(station_time_tuples) - 1):
            station = station_time_tuples[i][0]
            next_station = station_time_tuples[i + 1][0]
            value = calc_diff_in_time(
                station_time_tuples[i + 1][1], station_time_tuples[i][1])

            # Avoid duplicates
            if next_station in stop_time_dict and station in stop_time_dict[next_station]:
                continue

            if station not in stop_time_dict:
                stop_time_dict[station] = {next_station: value}
            else:
                stop_time_dict[station].update({next_station: value})

    return stop_time_dict


def build_tram_network(stops_file_path, lines_file_path):
    with open(get_data_path('tramnetwork.json'), 'w', encoding='utf-8') as f:
        stops = create_tram_stops(stops_file_path)
        lines, times = create_tram_lines_and_times(lines_file_path)
        f.write(json.dumps({**{'stops': stops}, **
                            {'lines': lines}, **{'times': times}}, indent=4))


def get_data_path(*args):
    base = os.path.dirname(os.getcwd())
    path = os.path.join(base, 'data', *args)
    return path


def lines_via_stops(line_dict, stop):
    available_lines = list()
    for line in line_dict:
        if stop in line_dict[line]:
            available_lines.append(line)
    # TODO raise / return 'no stations for that line' if none found
    available_lines.sort(key=int)
    return available_lines


def lines_between_stops(line_dict, stop1, stop2):
    available_lines = list()
    for line in line_dict:
        if line in lines_via_stops(line_dict, stop1) and line in lines_via_stops(line_dict, stop2):
            available_lines.append(line)
    available_lines.sort(key=int)
    return available_lines


def time_between_stops(time_dict, line_dict, line_number, stop1, stop2):
    if line_number not in lines_between_stops(line_dict, stop1, stop2):
        print("Both stops do not appear on the given line!")
        return -1
    line = line_dict[line_number]

    time = 0
    if line.index(stop1) == line.index(stop2):
        return time
    visited_stops = line[min(line.index(stop1), line.index(stop2)):max(
        line.index(stop1), line.index(stop2)) + 1]

    for i in range(len(visited_stops) - 1):
        try:
            time += time_dict[visited_stops[i]][visited_stops[i + 1]]
        except KeyError:
            time += time_dict[visited_stops[i + 1]][visited_stops[i]]
    return time


def distance_between_stops(stop_dict, stop1, stop2):
    R = 6371.009
    d_lat = abs(float(stop_dict[stop1]["lat"]) -
                float(stop_dict[stop2]["lat"])) * (pi / 180)
    lat_m = ((float(stop_dict[stop1]["lat"]) +
             float(stop_dict[stop2]["lat"])) / 2) * (pi / 180)
    d_lon = abs(float(stop_dict[stop1]["lon"]) -
                float(stop_dict[stop2]["lon"])) * (pi / 180)
    return round(R * sqrt((d_lat ** 2) + (cos(lat_m) * d_lon) ** 2), 3)


def dialogue(tramnetwork_file_path):
    with open(get_data_path(tramnetwork_file_path), "r", encoding="utf-8") as f:
        tram_network = json.load(f)

    while True:
        ip = input("> ")
        command = ip.split(" ")
        try:
            cmd = is_valid_command(command)
            args = isc(ip)[0]
        except InvalidCommandException as e:
            print(e)
            print("Sorry, try again!")
            continue

        if cmd == "q":
            exit(0)
        if cmd == "v":
            print(args)
            print(lines_via_stops(tram_network["lines"], args))
        if cmd == "b":
            print(args)
            print(lines_between_stops(
                tram_network["lines"], args[0], args[1]))
        if cmd == "t":
            print(args)
            print(time_between_stops(
                tram_network["times"], tram_network["lines"], args[0], args[1], args[2]))
        if cmd == "d":
            print(args)
            print(distance_between_stops(
                tram_network["stops"], args[0], args[1]))




def is_valid_command(command):
    first_command = command[0].lower()
    if first_command == "quit":
        return "q"
    if first_command == "via":
        return "v"
    if first_command == "between":
        return "b"
    if first_command == "time":
        return "t"
    if first_command == "distance":
        return "d"
    raise InvalidCommandException(command[0])


def isc(command: str):
    via = re.findall(r"via ((?:[a-ö]+ ?)+)", command, flags=re.IGNORECASE)
    if via:
        return via

    between = re.findall(r"between ((?:[a-ö]+ ?)+) and ((?:[a-ö]+ ?)+)", command, flags=re.IGNORECASE)
    if between:
        return between

    time = re.findall(r"time with (\d+) from ((?:[a-ö]+ ?)+) to ((?:[a-ö]+ ?)+)", command, flags=re.IGNORECASE)
    if time:
        return time

    distance = re.findall(r"distance from ((?:[a-ö]+ ?)+) to ((?:[a-ö]+ ?)+)", command, flags=re.IGNORECASE)
    if distance:
        return distance

def main():
    if 'init' in sys.argv:
        print("Creating tram network...")
        build_tram_network(TRAMSTOPS, TRAMLINES)
        print('Tram network created!')
    else:
        dialogue(TRAMNETWORK)


if __name__ == "__main__":
    main()
