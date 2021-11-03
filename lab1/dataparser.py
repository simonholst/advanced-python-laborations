import json


def build_tram_stops(jsonobject):
    x = json.load(jsonobject)
    print(x)


with open("data/tramstops.json", 'r') as file:
    build_tram_stops(file)
