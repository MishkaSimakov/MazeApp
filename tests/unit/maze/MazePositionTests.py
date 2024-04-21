import unittest
from copy import copy

from src.Maze import MazePosition


class MazePositionTests(unittest.TestCase):
    def test_copy_works(self):
        position = MazePosition(0, 0)
        position_copy = copy(position)

        position_copy.x = 10

        self.assertEqual(position_copy.x, 10)
        self.assertEqual(position.x, 0)

    def test_position_is_hashable(self):
        position = MazePosition(0, 0)
        try:
            hash(position)
        except:
            self.fail("MazePosition object must be hashable")

    def test_position_is_comparable(self):
        position = MazePosition(0, 0)

        self.assertNotEqual(position, MazePosition(0, 1))
        self.assertNotEqual(position, MazePosition(1, 0))
        self.assertEqual(position, MazePosition(0, 0))

    def test_position_support_arithmetics(self):
        position = MazePosition(0, 0)

        position += MazePosition(10, 20)
        self.assertEqual(position, MazePosition(10, 20))

        position *= 2
        self.assertEqual(position, MazePosition(20, 40))

        position -= MazePosition(30, 40)
        self.assertEqual(position, MazePosition(-10, 0))

    def test_position_return_neighbours_correctly(self):
        position = MazePosition(0, 0)

        self.assertEqual(position.left(), MazePosition(-1, 0))
        self.assertEqual(position.right(), MazePosition(1, 0))
        self.assertEqual(position.top(), MazePosition(0, -1))
        self.assertEqual(position.bottom(), MazePosition(0, 1))
