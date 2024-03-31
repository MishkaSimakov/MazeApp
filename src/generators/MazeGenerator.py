from abc import ABC, abstractmethod
from src.Maze import MazeConfig, Maze


class MazeGenerator(ABC):
    @abstractmethod
    def generate(self, config: MazeConfig) -> Maze:
        pass
