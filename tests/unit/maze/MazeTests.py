import unittest
from copy import copy

from src.Maze import MazeConfig, Maze, MazePosition, Direction


class MazeTests(unittest.TestCase):
    def setUp(self):
        self.maze_config = MazeConfig(width=10, height=15)
        self.maze = Maze(self.maze_config)

    def test_it_calculates_walls_count(self):
        self.assertEqual(self.maze.get_walls_count(), 275)

    def test_it_checks_for_correct_storage_size(self):
        self.assertEqual(len(self.maze.walls), self.maze.get_walls_count())
        self.assertTrue(self.maze.is_correct())

        self.maze.walls = []

        self.assertFalse(self.maze.is_correct())

    def test_it_calculates_cells_count(self):
        self.assertEqual(self.maze.get_cells_count(), 10 * 15)

    def test_it_calculates_wall_index(self):
        self.assertEqual(self.maze.get_wall_index(MazePosition(0, 0), Direction.RIGHT), 0)
        self.assertEqual(self.maze.get_wall_index(MazePosition(5, 5), Direction.LEFT), 99)
        self.assertEqual(self.maze.get_wall_index(MazePosition(4, 10), Direction.DOWN), 203)
        self.assertEqual(self.maze.get_wall_index(MazePosition(7, 2), Direction.UP), 35)

    def test_it_checks_for_wall_existence_inside(self):
        self.assertTrue(self.maze.has_wall(MazePosition(5, 5), Direction.DOWN))
        self.assertTrue(self.maze.has_wall(MazePosition(7, 3), Direction.UP))

        self.maze.walls[self.maze.get_wall_index(MazePosition(7, 3), Direction.UP)] = False

        self.assertFalse(self.maze.has_wall(MazePosition(7, 3), Direction.UP))

    def test_it_checks_for_wall_existence_on_border(self):
        self.assertTrue(self.maze.has_wall(MazePosition(0, 0), Direction.LEFT))
        self.assertTrue(self.maze.has_wall(MazePosition(0, 0), Direction.UP))

        self.assertTrue(self.maze.has_wall(MazePosition(9, 7), Direction.RIGHT))

        self.assertTrue(self.maze.has_wall(MazePosition(9, 14), Direction.DOWN))

    def test_it_checks_for_wall_existence_outside(self):
        self.assertFalse(self.maze.has_wall(MazePosition(-1, 0), Direction.LEFT))
        self.assertFalse(self.maze.has_wall(MazePosition(0, -1), Direction.UP))

    def test_it_checks_if_point_inside(self):
        self.assertTrue(self.maze.is_inside(MazePosition(0, 0)))
        self.assertTrue(self.maze.is_inside(MazePosition(0, 14)))
        self.assertTrue(self.maze.is_inside(MazePosition(9, 14)))
        self.assertTrue(self.maze.is_inside(MazePosition(9, 0)))
        self.assertTrue(self.maze.is_inside(MazePosition(5, 7)))

        self.assertFalse(self.maze.is_inside(MazePosition(-1, 0)))
        self.assertFalse(self.maze.is_inside(MazePosition(0, -1)))
        self.assertFalse(self.maze.is_inside(MazePosition(10, 5)))
        self.assertFalse(self.maze.is_inside(MazePosition(0, 15)))
        self.assertFalse(self.maze.is_inside(MazePosition(-1, 15)))
