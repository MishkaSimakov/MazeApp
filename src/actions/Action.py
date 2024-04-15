from abc import ABC, abstractmethod
from argparse import Namespace


class Action(ABC):
    """
    This abstract class represents action that program can do.
    Command line are used to call this actions. Fields `name` and `help`
    are used by argparse module to give additional information about each action.
    """

    name: str
    help: str

    @staticmethod
    @abstractmethod
    def add_subparser(parser):
        """
        Adds subparser for main argparse module parser.
        Subparser handle arguments for this action.
        """
        pass

    @staticmethod
    @abstractmethod
    def handle(args: Namespace):
        """Handle call of this action."""
        pass
