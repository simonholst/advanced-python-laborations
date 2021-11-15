import copy
import itertools
import unittest
from tramdata import *

TRAM_FILE = 'tramnetwork.json'
TRAM_LINES = 'tramlines.txt'


class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(get_data_path(TRAM_FILE), 'r', encoding='utf-8') as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    def test_lines_correct_group(self):
        with open(get_data_path(TRAM_LINES), 'r', encoding='utf-8') as f:
            text_lines = f.read()
            text_lines = text_lines.split("\n\n")
            i = 0
            for line in self.linedict:
                current = text_lines[i].split("\n")
                del current[0]
                for stop in self.linedict[line]:
                    self.assertIn(stop, current[0], msg=stop + 'not in tramlines.txt on line ' + str(current[0]))
                    del current[0]
                self.assertTrue(len(current) == 0)
                i += 1

    def test_max_distance(self):
        max_distance = 20
        for stop1, stop2 in list(itertools.combinations(list(self.stopdict), 2)):
            self.assertLess(distance_between_stops(self.stopdict, stop1, stop2),
                            max_distance,
                            msg=f"The distance between {stop1} and stop{2} is greater than {max_distance} km")

    def test_same_time(self):
        for line_number in self.linedict:
            for stop1, stop2 in list(itertools.combinations(self.linedict[line_number], 2)):
                self.assertEqual(time_between_stops(self.timedict, self.linedict, line_number, stop1, stop2),
                                 time_between_stops(self.timedict, self.linedict, line_number, stop2, stop1),
                                 msg=f"Time between {stop1} to {stop2} is not equal to time between {stop2} to {stop1}")



if __name__ == '__main__':
    unittest.main()
