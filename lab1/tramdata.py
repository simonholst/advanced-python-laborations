import json
import os
import re
import sys
from math import pi, sqrt, cos
from typing import List, Tuple
from invalidinputexception import InvalidInputException

TRAMLINES = 'tramlines.txt'
TRAMSTOPS = 'tramstops.json'
TRAMNETWORK = 'tramnetwork.json'


def build_tram_stops(json_object) -> dict:
    stops = json.load(json_object)
    return {stop.lower(): {'lat': stops[stop]["position"][0], 'lon': stops[stop]["position"][1]} for stop in stops}


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
    stops = re.compile(r"(?:[a-ö]+ ?)+\S", flags=re.IGNORECASE).findall(line)
    for i in range(len(stops)):
        stops[i] = stops[i].lower()
    return stops


def calc_diff_in_time(now: str, previous: str) -> int:
    mins100, mins = now.split(":")
    prev_mins100, prev_mins = previous.split(":")
    return (int(mins100) - int(prev_mins100)) * 100 + (int(mins) - int(prev_mins))


def create_tram_stops(file_path: str) -> dict:
    with open(get_data_path(file_path), 'r', encoding='utf-8') as f:
        return build_tram_stops(f)


def create_tram_lines_and_times(file_path: str):
    with open(get_data_path(file_path), 'r', encoding='utf-8') as f:
        return build_tram_lines_and_times(f)


def stations_and_times_list(expr: str) -> List[tuple]:
    return re.compile(r"((?:[a-ö]+ ?)+\S) *(\d\d:\d\d)", flags=re.IGNORECASE).findall(expr)


def build_tram_times(tram_lines: List[str]) -> dict:
    stop_time_dict = dict()
    for line in tram_lines:
        station_time_tuples = stations_and_times_list(line)
        for i in range(len(station_time_tuples) - 1):
            station = station_time_tuples[i][0].lower()
            next_station = station_time_tuples[i + 1][0].lower()
            value = calc_diff_in_time(station_time_tuples[i + 1][1],
                                      station_time_tuples[i][1])

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
        f.write(json.dumps({**{'stops': stops},
                            **{'lines': lines},
                            **{'times': times}}, indent=4))



def get_data_path(*args):
    base = os.path.dirname(os.getcwd())
    path = os.path.join(base, 'data', *args)
    return path


def lines_via_stops(line_dict, stop):
    available_lines = list()

    for line in line_dict:
        if stop.lower() in line_dict[line]:
            available_lines.append(line)

    if available_lines:
        available_lines.sort(key=int)
        return available_lines

    raise InvalidInputException(f"No line travels by: {stop}")


def lines_between_stops(line_dict, stop1, stop2):
    available_lines = list()
    for line in line_dict:
        if line in lines_via_stops(line_dict, stop1) and line in lines_via_stops(line_dict, stop2):
            available_lines.append(line)
    available_lines.sort(key=int)
    return available_lines


def time_between_stops(time_dict, line_dict, line_number, stop1, stop2):
    check_valid_line_num(line_dict, line_number)

    stop1, stop2 = stop1.lower(), stop2.lower()

    if stop1 == stop2:
        return 0

    check_if_line_between_stops(line_dict, line_number, stop1, stop2)
    line = line_dict[line_number]

    return calculate_time_between(line, stop1, stop2, time_dict)


def calculate_time_between(line, stop1, stop2, time_dict):
    time = 0
    visited_stops = line[min(line.index(stop1), line.index(stop2)):max(
        line.index(stop1), line.index(stop2)) + 1]
    for i in range(len(visited_stops) - 1):
        try:
            time += time_dict[visited_stops[i]][visited_stops[i + 1]]
        except KeyError:
            time += time_dict[visited_stops[i + 1]][visited_stops[i]]
    return time


def check_if_line_between_stops(line_dict, line_number, stop1, stop2):
    if line_number not in lines_between_stops(line_dict, stop1, stop2):
        raise InvalidInputException(
            f"Line {line_number} does not travel between {stop1} and {stop2}")


def check_valid_line_num(line_dict, line_number):
    if line_number not in line_dict:
        raise InvalidInputException(f"Line {line_number} does not exist")


def distance_between_stops(stop_dict, stop1, stop2):
    stop1 = stop1.lower()
    stop2 = stop2.lower()

    R = 6371.009
    try:
        d_lat = abs(float(stop_dict[stop1]["lat"]) -
                    float(stop_dict[stop2]["lat"])) * (pi / 180)
        lat_m = ((float(stop_dict[stop1]["lat"]) +
                  float(stop_dict[stop2]["lat"])) / 2) * (pi / 180)
        d_lon = abs(float(stop_dict[stop1]["lon"]) -
                    float(stop_dict[stop2]["lon"])) * (pi / 180)
    except KeyError as e:
        raise InvalidInputException(f"No such location found: {e}")

    return round(R * sqrt((d_lat ** 2) + (cos(lat_m) * d_lon) ** 2), 3)


def dialogue(tramnetwork_file_path):
    with open(get_data_path(tramnetwork_file_path), "r", encoding="utf-8") as f:
        tram_network = json.load(f)

    while True:
        try:
            print(execute_command(input("> "), tram_network))
        except InvalidInputException as e:
            print(e)
            print("Please try again!")
            continue


def execute_command(user_input, tram_network):
    via = re.findall(r"via ((?:[a-ö]+ ?)+)", user_input, flags=re.IGNORECASE)
    if via:
        return lines_via_stops(tram_network['lines'], via[0])

    between = re.findall(
        r"between ((?:[a-ö]+ ?)+) and ((?:[a-ö]+ ?)+)", user_input, flags=re.IGNORECASE)
    if between:
        return lines_between_stops(tram_network['lines'], between[0][0], between[0][1])

    time = re.findall(
        r"time with (\d+) from ((?:[a-ö]+ ?)+) to ((?:[a-ö]+ ?)+)", user_input, flags=re.IGNORECASE)
    if time:
        return time_between_stops(tram_network['times'], tram_network['lines'], time[0][0], time[0][1], time[0][2])

    distance = re.findall(
        r"distance from ((?:[a-ö]+ ?)+) to ((?:[a-ö]+ ?)+)", user_input, flags=re.IGNORECASE)
    if distance:
        return distance_between_stops(tram_network['stops'], distance[0][0], distance[0][1])

    if user_input == "quit":
        exit(0)

    raise InvalidInputException(
        f"Invalid input. Unknown command: '{user_input.split()[0]}'")


def create_network():
    print("Starting tram network creation...")
    build_tram_network(TRAMSTOPS, TRAMLINES)
    print('Tram network created!')


def main():
    if 'init' in sys.argv:
        create_network()
    else:
        try:
            dialogue(TRAMNETWORK)
        except FileNotFoundError as e:
            print(f"No tram network found at: {e.filename}")
            create_network()
            dialogue(TRAMNETWORK)


if __name__ == "__main__":
    main()
