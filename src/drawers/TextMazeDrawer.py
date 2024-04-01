from typing import Optional

from src.Maze import Maze, MazePosition, Direction, ThickMaze
from enum import Enum


class TextMazeDrawMode(Enum):
    THIN = 0
    THICK = 1


class TextMazeDrawer:
    __symbols: list[str] = [
        "x",  # 0000
        "╵",  # 0001
        "╶",  # 0010
        "└",  # 0011
        "╷",  # 0100
        "│",  # 0101
        "┌",  # 0110
        "├",  # 0111
        "╴",  # 1000
        "┘",  # 1001
        "─",  # 1010
        "┴",  # 1011
        "┐",  # 1100
        "┤",  # 1101
        "┬",  # 1110
        "┼",  # 1111
    ]

    def __get_character_for_cell(self, maze: Maze, position: MazePosition) -> str:
        mask = 0

        offsets_and_directions = [
            (MazePosition(-1, -1), Direction.RIGHT),
            (MazePosition(0, -1), Direction.DOWN),
            (MazePosition(0, 0), Direction.LEFT),
            (MazePosition(-1, 0), Direction.UP)
        ]

        for index, (offset, direction) in enumerate(offsets_and_directions):
            if not maze.has_wall(position + offset, direction):
                continue

            mask += 1 << index

        return self.__symbols[mask]

    def draw(self, maze: Maze) -> list[str]:
        result = [""] * (maze.config.height + 1)

        for y in range(maze.config.height + 1):
            for x in range(maze.config.width + 1):
                result[y] += self.__get_character_for_cell(maze, MazePosition(x, y))

        return result


class TextThickMazeDrawer:
    @staticmethod
    def __draw_thick_maze(maze: ThickMaze, solution: Optional[list[MazePosition]]) -> list[str]:
        if solution is None:
            solution = []

        solution_set = set(solution)
        result = [""] * maze.config.height

        for y in range(maze.config.height):
            for x in range(maze.config.width):
                character = " "

                if maze.maze[x][y]:
                    character = "█"
                elif MazePosition(x // 2, y // 2) in solution_set:
                    character = "x"

                result[y] += character

        return result

    @staticmethod
    def draw(maze: Maze, solution: list[MazePosition]):
        thick_maze = ThickMaze.from_thin_maze(maze)

        return TextThickMazeDrawer.__draw_thick_maze(thick_maze, solution)
