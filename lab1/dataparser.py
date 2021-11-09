import json
import re
from typing import List, Tuple


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


def create_tram_stops() -> dict:
    return apply_func_to_file(build_tram_stops, "data/tramstops.json")


def create_tram_lines_and_times() -> dict:
    return apply_func_to_file(build_tram_lines_and_times, "data/tramlines.txt")


def apply_func_to_file(func, path: str):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            return func(file)
    except FileNotFoundError:
        with open('../' + path, 'r', encoding="utf-8") as file:
            return func(file)


def stations_and_times_list(expr: str) -> List[tuple]:
    # flag = case insensitive
    return re.compile(r"((?:[a-öA-Ö]+ ?)+\S) *(\d\d:\d\d)", flags=re.IGNORECASE).findall(expr)


def build_tram_times(tram_lines: List[str]) -> dict:
    # FIXME maybe change to using dict() operation on the list of tuples
    stop_time_dict = dict()
    for line in tram_lines:
        station_time_tuples = stations_and_times_list(line)
        for i in range(len(station_time_tuples) - 1):
            station = station_time_tuples[i][0]
            next_station = station_time_tuples[i+1][0]
            value = calc_diff_in_time(
                station_time_tuples[i+1][1], station_time_tuples[i][1])

            # Avoid duplicates
            if next_station in stop_time_dict and station in stop_time_dict[next_station]:
                continue

            if station not in stop_time_dict:
                stop_time_dict[station] = {next_station: value}
            else:
                stop_time_dict[station].update({next_station: value})

    return stop_time_dict


def lines_via_stops(line_dict, stop):
    available_lines = list()
    for line in line_dict:
        if stop in line_dict[line]:
            available_lines.append(line)
    available_lines.sort(key=int)
    return available_lines


def lines_between_stops(line_dict, stop1, stop2):
    available_lines = list()
    for line in line_dict:
        if line in lines_via_stops(line_dict, stop1) and line in lines_via_stops(line_dict, stop2):
            available_lines.append(line)
    available_lines.sort(key=int)
    return available_lines


def time_between_stops(time_dict, line: dict, stop1, stop2):
    # TODO Should rerun the method until valid values are given
    if not list(line)[0] in lines_between_stops(line, stop1, stop2):
        print("Both stops do not appear on the given line!")
        return -1

    time = 0
    index1 = line[list(line)[0]].index(stop1)
    index2 = line[list(line)[0]].index(stop2)

    if index1 > index2:
        visited_stops = line[list(line)[0]][index2:index1 + 1]
    elif index1 < index2:
        visited_stops = line[list(line)[0]][index1:index2 + 1]
    else:
        return time

    for i in range(len(visited_stops) - 1):
        try:
            time += time_dict[visited_stops[i]][visited_stops[i + 1]]
        except KeyError:
            time += time_dict[visited_stops[i + 1]][visited_stops[i]]
    return time


def distance_between_stops(stop_dict, stop1, stop2):

    pass


def main():
    stops = create_tram_stops()
    lines, times = create_tram_lines_and_times()


if __name__ == "__main__":
    main()
