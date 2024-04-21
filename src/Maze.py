from enum import Enum
from copy import copy


class MazeConfig:
    """
    This class stores information about maze dimensions: width and height
    """
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class MazePosition:
    """
    This class represents position in maze. It acts like 2-D integer vector
    but has some methods specifically for mazes.
    """
    x: int
    y: int

    @staticmethod
    def none() -> 'MazePosition':
        """
        Returns MazePosition that represents absence of position.
        (such position must not appear as a valid position in maze)
        """
        return MazePosition(x=-1, y=-1)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __copy__(self) -> 'MazePosition':
        return MazePosition(self.x, self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: 'MazePosition') -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: 'MazePosition') -> 'MazePosition':
        return MazePosition(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'MazePosition') -> 'MazePosition':
        return MazePosition(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"MazePosition(x={self.x}, y={self.y})"

    def __mul__(self, scalar: int) -> 'MazePosition':
        return MazePosition(self.x * scalar, self.y * scalar)

    def left(self) -> 'MazePosition':
        """Returns left neighbor of current position"""
        return self + MazePosition(-1, 0)

    def right(self) -> 'MazePosition':
        """Returns right neighbor of current position"""
        return self + MazePosition(1, 0)

    def top(self) -> 'MazePosition':
        """Returns top neighbor of current position"""
        return self + MazePosition(0, -1)

    def bottom(self) -> 'MazePosition':
        """Returns bottom neighbor of current position"""
        return self + MazePosition(0, 1)


class Direction(Enum):
    """
    Represents four main directions in 2-D plane.
    Directions are strongly connected to MazePosition class.
    Value of each direction is MazePosition such that addition of this position
    will move you into this direction.
    """

    UP = MazePosition(0, -1)
    RIGHT = MazePosition(1, 0)
    DOWN = MazePosition(0, 1)
    LEFT = MazePosition(-1, 0)

    @staticmethod
    def index_by_value(value: MazePosition) -> int:
        """Returns index of direction associated with given MazePosition"""
        if value.y == -1:
            return 0
        elif value.x == 1:
            return 1
        elif value.y == 1:
            return 2
        else:
            return 3


class Maze:
    """
    Represents a thin maze. 'Thin' means that walls located between cells.
    """

    # walls between cells
    walls: list[bool]
    config: MazeConfig

    def __init__(self, config: MazeConfig):
        self.config = config
        self.walls = [True] * self.get_walls_count()

    def is_correct(self) -> bool:
        """Checks if class internal structure is valid."""
        return len(self.walls) == self.get_walls_count()

    def get_walls_count(self):
        """Returns total walls count in this maze (count even removed walls)"""
        return ((self.config.width - 1) * self.config.height
                + self.config.width * (self.config.height - 1))

    def get_cells_count(self):
        """Returns cells count in this maze"""
        return self.config.width * self.config.height

    def get_wall_index(self, cell: MazePosition, direction: Direction) -> int:
        """Returns index of wall in walls array that is located in given direction from given cell."""
        cell_copy = copy(cell)

        if direction == Direction.LEFT:
            direction = Direction.RIGHT
            cell_copy.x -= 1

        if direction == Direction.UP:
            direction = Direction.DOWN
            cell_copy.y -= 1

        if direction == Direction.RIGHT:
            return cell_copy.x + cell_copy.y * (2 * self.config.width - 1)

        # direction == Direction.DOWN
        return self.config.width - 1 + cell_copy.x + cell_copy.y * (2 * self.config.width - 1)

    def has_wall(self, cell: MazePosition, direction: Direction) -> bool:
        """Checks if wall exists in given direction from given cell."""
        first_outside = not self.is_inside(cell)
        second_outside = not self.is_inside(direction.value + cell)
        if first_outside != second_outside:
            return True

        if first_outside or second_outside:
            return False

        return self.walls[self.get_wall_index(cell, direction)]

    def is_inside(self, position: MazePosition) -> bool:
        """Check if given MazePosition is located inside maze."""
        return 0 <= position.x < self.config.width and 0 <= position.y < self.config.height

    def __eq__(self, other: 'Maze') -> bool:
        """Compare two mazes for equality."""
        if self.config.width != other.config.width or self.config.height != other.config.height:
            return False

        return self.walls == other.walls


class ThickMazeCellType(Enum):
    """Represents cell types for thick maze."""
    EMPTY = 0
    WALL = 1
    PATH = 2


class ThickMaze:
    """
    Represents thick maze. 'Thick' means that walls are also represented by cells.
    ThickMazeCellType exists for storing type of cell. It can be empty or wall might be in it.
    Also, there is a PATH maze cell type that is only used for solution drawing in this type of maze.
    """
    maze: list[list[ThickMazeCellType]]
    config: MazeConfig

    def __init__(self, config: MazeConfig):
        self.config = config

        self.maze = [[ThickMazeCellType.EMPTY] * config.height for _ in range(config.width)]

    @staticmethod
    def from_thin_maze(thin_maze: Maze):
        """Initialize thick maze from thin maze. This method copy value so new maze will be independent of old."""
        width = thin_maze.config.width * 2 + 1
        height = thin_maze.config.height * 2 + 1

        thick_maze = ThickMaze(MazeConfig(width, height))

        for x in range(width):
            for y in range(height):
                has_wall = False

                if x % 2 == y % 2:
                    has_wall = x % 2 == 0
                elif x % 2 == 0:
                    has_wall = thin_maze.has_wall(MazePosition(x // 2 - 1, y // 2), Direction.RIGHT)
                elif y % 2 == 0:
                    has_wall = thin_maze.has_wall(MazePosition(x // 2, y // 2 - 1), Direction.DOWN)

                if has_wall:
                    thick_maze.maze[x][y] = ThickMazeCellType.WALL

        return thick_maze
