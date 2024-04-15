import unittest

from src.Maze import MazeConfig
from src.generators.MazeGenerator import MazeGenerator
from src.solvers.BFSMazeSolver import BFSMazeSolver


class MazeGeneratorTests(unittest.TestCase):
    generator: MazeGenerator

    def __init__(self, generator: MazeGenerator):
        super().__init__()
        self.generator = generator

    def setUp(self):
        self.config = MazeConfig(10, 15)

    def test_it_generate_valid_maze(self):
        maze = self.generator.generate(self.config)

        self.assertTrue(maze.is_correct())

    def test_there_is_solution_in_generated_maze(self):
        # we generate many mazes because they are random
        for i in range(100):
            maze = self.generator.generate(self.config)

            # we assume that maze solver is already tested
            try:
                BFSMazeSolver.solve(maze)
            except:
                self.fail("Maze generated by generator doesn't have any solution.")
