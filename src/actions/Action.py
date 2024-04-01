from abc import ABC, abstractmethod
from argparse import Namespace


class Action(ABC):
    name: str
    help: str

    @staticmethod
    @abstractmethod
    def add_subparser(parser):
        pass

    @staticmethod
    @abstractmethod
    def handle(args: Namespace):
        pass
