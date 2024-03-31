import json

from src.Maze import Maze, MazeConfig
from typing import Optional


class MazeFileManager:
    @staticmethod
    def read_from_file(filename: str) -> Optional[Maze]:
        try:
            with open(filename) as file:
                content = json.loads(file.readline())

                width = content["width"]
                height = content["height"]
                maze_walls = content["walls"]

            maze = Maze(MazeConfig(width, height))
            maze.walls = maze_walls

            if not maze.is_correct():
                raise Exception("Invalid maze file.")

            return maze
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def write_into_file(filename: str, maze: Maze) -> bool:
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
