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


# "C:/Users/Milvi/PycharmProjects/laboration-1/data/tramstops.json"
with open("C:/Users/Milvi/PycharmProjects/laboration-1/data/tramstops.json", 'r') as file:
    build_tram_stops(file)
