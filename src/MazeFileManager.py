import json

from src.Maze import Maze, MazeConfig
from typing import Optional


class MazeFileInvalidException(Exception):
    """Exception raised when you try to read maze from invalid maze file"""

    def __init__(self):
        super().__init__("Provided maze file is invalid.")


class MazeFileManager:
    """
    Read and save maze into file.
    """

    @staticmethod
    def read_from_file(filename: str) -> Optional[Maze]:
        """Read maze from file. Exception is thrown if file content is invalid."""

        with open(filename) as file:
            content = json.loads(file.readline())

            width = content["width"]
            height = content["height"]
            maze_walls = content["walls"]

        maze = Maze(MazeConfig(width, height))
        maze.walls = maze_walls

        if not maze.is_correct():
            raise MazeFileInvalidException()

        return maze

    @staticmethod
    def write_into_file(filename: str, maze: Maze) -> bool:
        """Write maze into file using json format."""

        try:
            content = json.dumps({
                "width": maze.config.width,
                "height": maze.config.height,
                "walls": maze.walls
            })

            with open(filename, "w") as file:
                file.write(content)

            return True
        except Exception as e:
            print(e)
            return False
