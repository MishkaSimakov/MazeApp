from abc import ABC, abstractmethod
from src.Maze import MazeConfig, Maze


class MazeGenerator(ABC):
    """This abstract class represents maze generation algorithms."""

    @abstractmethod
    def generate(self, config: MazeConfig) -> Maze:
        """Generate maze according to given config."""
        pass
