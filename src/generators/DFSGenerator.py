from src.Maze import *
from random import shuffle

from src.generators.MazeGenerator import MazeGenerator


class DFSGenerator(MazeGenerator):
    """
    Maze Generator that uses DFS algorithm to generate maze.
    DFS - depth-first search - means that algorithm goes in random direction as far as it can
    and only when no directions are available goes back.
    """

    def generate(self, config: MazeConfig) -> Maze:
        maze = Maze(config)
        used = [[False] * config.height for _ in range(config.width)]
        history = [MazePosition(0, 0)]

        while len(history) != 0:
            current = history[-1]

            used[current.x][current.y] = True

            directions = list(Direction)
            shuffle(directions)

            for direction in directions:
                next_cell = current + direction.value
                if not maze.is_inside(next_cell) or used[next_cell.x][next_cell.y]:
                    continue

                history.append(next_cell)
                maze.walls[maze.get_wall_index(current, direction)] = False
                break
            else:
                history.pop()

        return maze
