import tempfile
import unittest

from src.Maze import MazeConfig
from src.MazeFileManager import MazeFileManager, MazeFileInvalidException
from src.generators.MazeGenerator import MazeGenerator
from src.solvers.BFSMazeSolver import BFSMazeSolver


class FileManagerTests(unittest.TestCase):
    valid_filename = "../../files/valid_maze.maze"
    invalid_filename = "../../files/invalid_maze.maze"

    temp_filename = "../../files/temp_maze.maze"

    def test_it_loads_valid_maze(self):
        maze = MazeFileManager.read_from_file(self.valid_filename)

        self.assertTrue(maze.is_correct())
        self.assertEqual(maze.config.width, 5)
        self.assertEqual(maze.config.height, 5)

        self.assertFalse(maze.walls[0])
        self.assertFalse(maze.walls[-1])

    def test_it_fails_to_load_invalid_maze(self):
        with self.assertRaises(MazeFileInvalidException):
            MazeFileManager.read_from_file(self.invalid_filename)

    def test_it_writes_maze(self):
        maze = MazeFileManager.read_from_file(self.valid_filename)

        filename = tempfile.NamedTemporaryFile().name

        MazeFileManager.write_into_file(filename, maze)
        second_maze = MazeFileManager.read_from_file(filename)

        self.assertEqual(maze, second_maze)
