#-*- coding: utf-8 -*-
import signal, unittest
from datetime import datetime
from metadata_extractor import *
from metadata_extractor.converter import *
from os.path import abspath, dirname, realpath

path_to_directory_of_this_file = dirname(realpath(__file__))

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise OSError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

class TestParsingMethods(unittest.TestCase):

    def test_word_doc(self):
        layers = extract_metadata("/tmp/source.docx")
        self.assertTrue(len(layers) > 0)
        save_metadata(layers, _format="ISO 19115-2", path_to_dir="/tmp")

    def test_split_by_indices(self):

        self.assertEqual(split_by_indices([2,3,4], positions=[4], offset=2), [[2,3],[4]])

        iterable = [0,1,2,3,4]
        split = split_by_indices(iterable, [2])
        self.assertEqual(split, [[0,1,],[2,3,4]])

        split = [[0, 1], [2, 3, 4]]
        split = split_by_indices(split, [4])
        self.assertEqual(split, [[[0,1]],[[2,3],[4]]])

if __name__ == '__main__':
    unittest.main()
