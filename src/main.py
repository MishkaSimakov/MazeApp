import random

from src.MazeFileManager import MazeFileManager
from src.drawers.TextMazeDrawer import TextMazeDrawer, TextMazeDrawMode
from src.generators.DFSGenerator import DFSGenerator
from src.Maze import *

if __name__ == "__main__":
    gen = DFSGenerator()
    maze = gen.generate(MazeConfig(width=50, height=10))

    path = "/Users/mihailsimakov/Documents/Programs/MazeGenerator/maze.maze"
    MazeFileManager.write_into_file(path, maze)
    read_maze = MazeFileManager.read_from_file(path)

    drawer = TextMazeDrawer(draw_mode=TextMazeDrawMode.THIN)
    print(*drawer.draw(read_maze), sep="\n")
