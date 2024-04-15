from typing import Optional

from src.Maze import Maze, MazePosition, Direction


class BFSMazeSolver:
    """
    Use BFS algorithm to find solution for any maze.
    BFS - breadth-first search - visit each neighbour and only then go deeper.
    """

    @staticmethod
    def calculate_prev_cells(maze: Maze, begin: MazePosition, end: MazePosition) -> Optional[list[MazePosition]]:
        """
        This method go through all maze using BFS
        and for each cell store position from which it gets to this cell.
        """

        stack = [begin]
        prev = [MazePosition.none()] * maze.get_cells_count()
        prev[0] = begin

        used_count = 1

        while used_count < maze.get_cells_count():
            new_stack = []

            for cell in stack:
                for direction in Direction:
                    new_cell = cell + direction.value
                    index = new_cell.x + new_cell.y * maze.config.width

                    if index < 0 or index >= maze.get_cells_count():
                        continue

                    is_used = prev[index] != MazePosition.none()
                    if maze.has_wall(cell, direction) or is_used:
                        continue

                    prev[index] = cell
                    if new_cell == end:
                        return prev

                    new_stack.append(new_cell)
                    used_count += 1

            stack = new_stack

        return None

    @staticmethod
    def solve(maze: Maze) -> Optional[list[MazePosition]]:
        """
        This method solves maze.
        It uses `calculate_prev_cells` method that calculates BFS path in maze,
        and then using this information build a path from start to end.
        By default, start is (0, 0), end is (width - 1, height - 1)
        """

        path_begin = MazePosition(0, 0)
        path_end = MazePosition(maze.config.width - 1, maze.config.height - 1)
        prev = BFSMazeSolver.calculate_prev_cells(maze, path_begin, path_end)

        if prev is None:
            return None

        result = []
        current = path_end
        while current != path_begin:
            result.append(current)
            current = prev[current.x + current.y * maze.config.width]

        result.append(path_begin)

        return result
