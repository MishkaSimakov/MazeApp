from typing import Optional
from colorama import Fore, Style

from src.Maze import Maze, MazePosition, Direction, ThickMaze, ThickMazeCellType


class TextMazeDrawer:
    """
    Use special symbols to print thin maze into console.
    This class also supports path drawing.
    Colorama library is used for colored output.
    """

    __symbols: list[str] = [
        " ",  # 0000
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

    @staticmethod
    def __get_mask_for_cell(maze: Maze, position: MazePosition) -> int:
        """
        Special symbols are used for walls. Each special symbol has some connection:
        top, right, bottom or left. This method calculates connections required for wall
        in given point (according to its neighbors) and return symbol index for this wall.
        """
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

        return mask

    def __get_solution_path(self, solution: Optional[list[MazePosition]]) -> dict[MazePosition, str]:
        """
        Special symbols are used for solution path drawing.
        This method take solution and return dict that contain appropriate
        special symbol for each cell on the solution path.
        """
        result = dict()

        for index in range(len(solution)):
            position = solution[index] * 2 + MazePosition(1, 1)

            if index != len(solution) - 1:
                intermediate_position = solution[index + 1] + solution[index] + MazePosition(1, 1)
                offset = position - intermediate_position

                if offset == Direction.UP.value or offset == Direction.DOWN.value:
                    symbol_code = 1 << 0 | 1 << 2
                else:
                    symbol_code = 1 << 1 | 1 << 3
                result[intermediate_position] = Fore.CYAN + self.__symbols[symbol_code] + Style.RESET_ALL

            if index == 0 or index == len(solution) - 1:
                result[position] = Fore.CYAN + "⚑" + Style.RESET_ALL
                continue

            prev_offset = 1 << Direction.index_by_value(solution[index - 1] - solution[index])
            next_offset = 1 << Direction.index_by_value(solution[index + 1] - solution[index])
            offset = prev_offset | next_offset

            result[position] = Fore.CYAN + self.__symbols[offset] + Style.RESET_ALL

        return result

    def draw(self, maze: Maze, solution: Optional[list[MazePosition]] = None) -> list[str]:
        """Return text representation of given maze and (optionally) its solution."""

        if solution is None:
            solution = []

        spacing = 2 if len(solution) != 0 else 1

        result_width = maze.config.width * spacing
        result_height = maze.config.height * spacing

        result = [""] * (result_height + 1)

        solution_path = self.__get_solution_path(solution)

        for y in range(result_height + 1):
            for x in range(result_width + 1):
                position = MazePosition(x // spacing, y // spacing)

                if x % spacing == 0 and y % spacing == 0:
                    mask = self.__get_mask_for_cell(maze, position)
                    result[y] += self.__symbols[mask]
                    continue

                if MazePosition(x, y) in solution_path:
                    result[y] += solution_path[MazePosition(x, y)]
                    continue

                if x % spacing == 0:
                    top_mask = self.__get_mask_for_cell(maze, position) & (1 << 2)
                    bottom_mask = self.__get_mask_for_cell(maze, position.bottom()) & 1
                    result[y] += self.__symbols[top_mask + bottom_mask]
                elif y % spacing == 0:
                    left_mask = self.__get_mask_for_cell(maze, position) & (1 << 1)
                    right_mask = self.__get_mask_for_cell(maze, position.right()) & (1 << 3)
                    result[y] += self.__symbols[left_mask + right_mask]
                else:
                    result[y] += " "

        return result


class TextThickMazeDrawer:
    """
    Print thick maze into console. Walls and empty cells have equal size in this type of maze.
    """

    @staticmethod
    def draw(maze: Maze, solution: list[MazePosition]):
        thick_maze = ThickMaze.from_thin_maze(maze)

        if solution is None:
            solution = []

        for index in range(len(solution)):
            current_position = solution[index] * 2 + MazePosition(1, 1)
            thick_maze.maze[current_position.x][current_position.y] = ThickMazeCellType.PATH

            if index == len(solution) - 1:
                continue

            intermediate_position = solution[index + 1] + solution[index] + MazePosition(1, 1)
            thick_maze.maze[intermediate_position.x][intermediate_position.y] = ThickMazeCellType.PATH

        result = [""] * thick_maze.config.height

        for y in range(thick_maze.config.height):
            for x in range(thick_maze.config.width):
                character = " "

                if thick_maze.maze[x][y] == ThickMazeCellType.WALL:
                    character = "█"
                elif thick_maze.maze[x][y] == ThickMazeCellType.PATH:
                    character = "x"

                result[y] += character

        return result
