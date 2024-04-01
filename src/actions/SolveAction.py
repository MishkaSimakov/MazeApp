from argparse import Namespace

from src.actions.Action import Action


class SolveAction(Action):
    name = "solve"
    help = "solve help"

    @staticmethod
    def add_subparser(parser):
        subparser = parser.add_parser(SolveAction.name, help=SolveAction.help)
        subparser.add_argument('-f', type=str, help='file path')

    @staticmethod
    def handle(args: Namespace):
        print("solve", args)
