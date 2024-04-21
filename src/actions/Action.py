from abc import ABC, abstractmethod
from argparse import Namespace


class Action(ABC):
    """
    This abstract class represents action that program can do.
    Command line is used to call this actions. Fields `name` and `help`
    are used by argparse module to give additional information about each action.
    """

    name: str
    help: str

    @staticmethod
    @abstractmethod
    def add_subparser(parser):
        """
        Adds subparser for the main argparse module parser.
        Subparser handles arguments for this action.
        """
        pass

    @staticmethod
    @abstractmethod
    def handle(args: Namespace):
        """Handle call of this action."""
        pass
