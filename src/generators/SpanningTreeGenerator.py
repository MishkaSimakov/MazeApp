import random

from src.Maze import *
from src.generators.MazeGenerator import MazeGenerator


class SpanningTreeGenerator(MazeGenerator):
    def generate(self, config: MazeConfig) -> Maze:
        maze = Maze(config)

        directions = list(Direction)
        used = [[False] * config.height for _ in range(config.width)]

        random_point = MazePosition(
            x=random.randrange(0, config.width),
            y=random.randrange(0, config.height)
        )

        adjacent = [
            (random_point, Direction.UP),
        ]

        used[random_point.x][random_point.y] = True

        while len(adjacent) != 0:
            random_index = random.randrange(0, len(adjacent))
            adj_cell, adj_direction = adjacent[random_index]

            adjacent.remove((adj_cell, adj_direction))

            wall_index = maze.get_wall_index(adj_cell, adj_direction)

            if wall_index >= 0:
                maze.walls[wall_index] = False

            for direction in directions:
                next_cell = adj_cell - direction.value
                if not maze.is_inside(next_cell) or used[next_cell.x][next_cell.y]:
                    continue

                used[next_cell.x][next_cell.y] = True
                adjacent.append((next_cell, direction))

        return maze
