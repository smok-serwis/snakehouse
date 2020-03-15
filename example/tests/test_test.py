from example_module.test import times_two
from example_module.test2 import times_three
from example_module.test3.test3 import times_four
import unittest


class TestExample(unittest.TestCase):
    def test_two(self):
        self.assertEqual(times_two(2), 4)

    def test_three(self):
        self.assertEqual(times_three(2), 6)

    def test_four(self):
        self.assertEqual(times_four(2), 8)
