import pprint
import re
from dataparser import apply_func_to_file


def re_test(text_file):
    text = text_file.read()
    times = find_times(text)
    stations = find_station_names(text)
    both_dict = stations_and_times_dict(text)


def find_times(expr):
    return re.findall(r"\d\d:\d\d", expr)
    # \d matches a digit (equivalent to [0-9])
    # : matches the character :


def find_station_names(expr):
    return re.findall(r"[a-öA-Ö]+ ?[a-öA-Ö]+", expr)
    # + matches the previous token between one and unlimited times
    # ? matches the previous token between zero and one times
    # a-ö matches a single character in the range between a (index 97) and ö (index 246) (case sensitive)
    # A-Ö matches a single character in the range between A (index 65) and Ö (index 214) (case sensitive)


def stations_and_times_dict(expr):
    pattern = re.compile(r"([a-ö]+ ?[a-ö]+ ?[a-ö]+) *(\d\d:\d\d)",
                         flags=re.IGNORECASE)  # flag = case insensitive
    return dict(pattern.findall(expr))


def stations_and_times_list(expr):
    pattern = re.compile(r"([a-ö]+ ?[a-ö]+ ?[a-ö]+) *(\d\d:\d\d)",
                         flags=re.IGNORECASE)  # flag = case insensitive
    return pattern.findall(expr)


if __name__ == "__main__":
    apply_func_to_file(re_test, "data/tramlines.txt")

'''
Bra video: https://youtu.be/sa-TUpSx1JA
Han har också fler om re just i python, har inte tittat på allt själv men finns iaf vilket är nice
https://re101.com/ Schysst sida för att testa vad som matchar, klicka i Python under Flavor-fliken till vänster
'''

