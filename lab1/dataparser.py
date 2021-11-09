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
            value = calc_diff_in_time(station_time_tuples[i+1][1], station_time_tuples[i][1])

            # Avoid duplicates
            if next_station in stop_time_dict and station in stop_time_dict[next_station]:
                continue

            if station not in stop_time_dict:
                stop_time_dict[station] = {next_station: value}
            else:
                stop_time_dict[station].update({next_station: value})

    return stop_time_dict


def lines_via_stops(somedicts, stop):
    pass


def lines_between_stops(somedicts, stop1, stop2):
    pass


def time_between_stops(somedicts, line, stop1, stop2):
    pass


def distance_between_stops(somedicts, stop1, stop2):
    pass


def main():
    stops = create_tram_stops()
    lines, times = create_tram_lines_and_times()


if __name__ == "__main__":
    main()
