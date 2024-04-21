import unittest

from src.Maze import MazeConfig, MazePosition, Direction
from src.generators.DFSGenerator import DFSGenerator
from src.solvers.BFSMazeSolver import BFSMazeSolver, UnsolvableMazeException


class MazeSolverTests(unittest.TestCase):
    def setUp(self):
        self.config = MazeConfig(10, 15)

    def test_solution_is_correct(self):
        # we generate and solve many mazes

        for i in range(100):
            maze = DFSGenerator().generate(self.config)
            solution = BFSMazeSolver.solve(maze)[::-1]

            self.assertEqual(solution[0], MazePosition(0, 0))
            self.assertEqual(solution[-1], MazePosition(self.config.width - 1, self.config.height - 1))

            visited = set()

            for cell_index in range(len(solution) - 1):
                cell = solution[cell_index]
                next_cell = solution[cell_index + 1]
                direction = next_cell - cell

                try:
                    direction_name = Direction(direction)
                except ValueError:
                    self.fail("Path in solution must be continuous.")

                self.assertFalse(maze.has_wall(cell, direction_name))

                if cell in visited:
                    self.fail("Path visit same cell twice.")

                visited.add(cell)

    def test_it_raise_exception_when_maze_is_unsolvable(self):
        unsolvable = DFSGenerator().generate(self.config)
        corner = MazePosition(self.config.width - 1, self.config.height - 1)

        unsolvable.walls[unsolvable.get_wall_index(corner, Direction.LEFT)] = True
        unsolvable.walls[unsolvable.get_wall_index(corner, Direction.UP)] = True

        with self.assertRaises(UnsolvableMazeException):
            BFSMazeSolver.solve(unsolvable)
