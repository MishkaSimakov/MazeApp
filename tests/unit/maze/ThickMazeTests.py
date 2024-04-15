import unittest

from src.Maze import MazeConfig, Maze, MazePosition, Direction, ThickMaze, ThickMazeCellType


class ThickMazeTests(unittest.TestCase):
    def setUp(self):
        self.maze_config = MazeConfig(width=10, height=15)
        self.maze = Maze(self.maze_config)
        self.thick_maze = ThickMaze.from_thin_maze(self.maze)

    def test_it_copy_config(self):
        # thick maze doubles thin maze size
        self.assertEquals(self.thick_maze.config.width, self.maze.config.width * 2 + 1)
        self.assertEquals(self.thick_maze.config.height, self.maze.config.height * 2 + 1)

    def test_it_copy_walls_layout(self):
        self.assertEqual(self.thick_maze.maze[1][2], ThickMazeCellType.WALL)

        maze = Maze(self.maze_config)
        maze.walls[maze.get_wall_index(MazePosition(0, 0), Direction.DOWN)] = False

        thick_maze = ThickMaze.from_thin_maze(maze)

        self.assertEqual(thick_maze.maze[1][2], ThickMazeCellType.EMPTY)
