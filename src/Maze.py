from enum import Enum


class MazeConfig:
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class MazePosition:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: 'MazePosition') -> 'MazePosition':
        return MazePosition(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'MazePosition') -> 'MazePosition':
        return MazePosition(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"MazePosition(x={self.x}, y={self.y})"


class Direction(Enum):
    UP = MazePosition(0, -1)
    RIGHT = MazePosition(1, 0)
    DOWN = MazePosition(0, 1)
    LEFT = MazePosition(-1, 0)


class Maze:
    # walls between cells
    walls: list[bool]
    config: MazeConfig

    def __init__(self, config: MazeConfig):
        self.config = config
        self.walls = [True] * self.get_walls_count()

    def is_correct(self) -> bool:
        return len(self.walls) == self.get_walls_count()

    def get_walls_count(self):
        return ((self.config.width - 1) * self.config.height
                + self.config.width * (self.config.height - 1))

    def get_wall_index(self, cell: MazePosition, direction: Direction) -> int:
        if direction == Direction.LEFT:
            direction = Direction.RIGHT
            cell.x -= 1

        if direction == Direction.UP:
            direction = Direction.DOWN
            cell.y -= 1

        if direction == Direction.RIGHT:
            return cell.x + cell.y * (2 * self.config.width - 1)

        # direction == Direction.DOWN
        return self.config.width - 1 + cell.x + cell.y * (2 * self.config.width - 1)

    def has_wall(self, cell: MazePosition, direction: Direction) -> bool:
        first_outside = not self.is_inside(cell)
        second_outside = not self.is_inside(direction.value + cell)
        if first_outside != second_outside:
            return True

        if first_outside or second_outside:
            return False

        return self.walls[self.get_wall_index(cell, direction)]

    def is_inside(self, position: MazePosition) -> bool:
        return 0 <= position.x < self.config.width and 0 <= position.y < self.config.height


class ThickMaze:
    maze: list[list[bool]]
    config: MazeConfig

    def __init__(self, config: MazeConfig):
        self.config = config

        self.maze = [[False] * config.height for _ in range(config.width)]

    @staticmethod
    def from_thin_maze(thin_maze: Maze):
        width = thin_maze.config.width * 2 + 1
        height = thin_maze.config.height * 2 + 1

        thick_maze = ThickMaze(MazeConfig(width, height))

        for x in range(width):
            for y in range(height):
                if x % 2 == y % 2:
                    thick_maze.maze[x][y] = x % 2 == 0
                elif x % 2 == 0:
                    thick_maze.maze[x][y] = thin_maze.has_wall(MazePosition(x // 2 - 1, y // 2), Direction.RIGHT)
                elif y % 2 == 0:
                    thick_maze.maze[x][y] = thin_maze.has_wall(MazePosition(x // 2, y // 2 - 1), Direction.DOWN)

        return thick_maze
