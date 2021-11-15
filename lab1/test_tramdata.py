import copy
import itertools
import unittest
from tramdata import *
import random

TRAM_FILE = 'tramnetwork.json'
TRAM_LINES = 'tramlines.txt'


class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(get_data_path(TRAM_FILE), 'r', encoding='utf-8') as trams:
            self.tramdict = json.loads(trams.read())
            self.stopdict = self.tramdict['stops']
            self.linedict = self.tramdict['lines']
            self.timedict = self.tramdict['times']

    def test_stops_exist(self):
        stopset = {
            stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg=stop + ' not in stopdict')

    def test_lines_correct_group(self):
        with open(get_data_path(TRAM_LINES), 'r', encoding='utf-8') as f:
            text_lines = f.read()
            text_lines = text_lines.split("\n\n")
            i = 0
            for line in self.linedict:
                current = text_lines[i].split("\n")
                del current[0]
                for stop in self.linedict[line]:
                    self.assertIn(
                        stop, current[0].lower(), msg=stop + 'not in tramlines.txt on line ' + str(current[0]))
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
                                 time_between_stops(
                                     self.timedict, self.linedict, line_number, stop2, stop1),
                                 msg=f"Time between {stop1} to {stop2} is not equal to time between {stop2} to {stop1}")

    # The dialogue functions below test the array of user inputs, rather than the
    # concrete implementation itself. The main purpose of the tests is
    # to confirm that they don't raise an error. With asserts as a double check.

    def test_dialogue_via(self):
        for stop in self.stopdict:
            command = f"via {stop}"
            self.assertTrue(execute_command(command, self.tramdict),
                            msg=f"Did not find any lines for {stop}")

    def test_dialogue_between(self):
        max_n_lines = len(self.linedict)
        coms = list(itertools.combinations(list(self.stopdict), 2))

        for _ in range(100):
            stop1, stop2 = random.choice(coms)
            command = f"between {stop1} and {stop2}"

            self.assertLessEqual(len(execute_command(command, self.tramdict)),
                                 max_n_lines,
                                 msg=f"The number of available lines exceeds the number of total lines between\
                                        {stop1} and {stop2}")

    def test_dialogue_time(self):
        max_time = 99
        line_numbers = self.linedict.keys()

        for line_number in line_numbers:
            coms = list(itertools.combinations(
                list(self.linedict[line_number]), 2))
            for _ in range(10):
                stop1, stop2 = random.choice(coms)
                command = f"time with {line_number} from {stop1} to {stop2}"
                self.assertLess(execute_command(command, self.tramdict),
                                max_time,
                                msg=f"Travel time from {stop1} to {stop2} is greater than {max_time} min")

    def test_dialogue_distance(self):
        max_distance = 20
        coms = list(itertools.combinations(list(self.stopdict), 2))

        for _ in range(100):
            stop1, stop2 = random.choice(coms)
            command = f"distance from {stop1} to {stop2}"
            self.assertLess(execute_command(command, self.tramdict),
                            max_distance,
                            msg=f"The distance between {stop1} and stop{2} is greater than {max_distance} km")

    def test_invalid_input(self):
        invalid_commands = ["not_valid_command", "via my house", "between Chalmers and Malmö", "distance from here to there",
                            "time with 14 from Chalmers to Brunnsparken"]
        for invalid_command in invalid_commands:
            with self.assertRaises(InvalidInputException):
                execute_command(invalid_command, self.tramdict)


if __name__ == '__main__':
    unittest.main()
