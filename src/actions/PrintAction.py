from argparse import Namespace

from src.MazeFileManager import MazeFileManager
from src.actions.Action import Action
from src.drawers.TextMazeDrawer import TextMazeDrawer, TextMazeDrawMode


class PrintAction(Action):
    name = "print"
    help = "Prints maze stored in file."

    @staticmethod
    def add_subparser(parser):
        subparser = parser.add_parser(PrintAction.name, help=PrintAction.help)
        subparser.add_argument('-f', dest="path", type=str, help='File to read maze from.', required=True)

    @staticmethod
    def handle(args: Namespace):
        maze = MazeFileManager.read_from_file(args.path)

        if not maze:
            print("Error occurred while reading file.")
            return

        print(*TextMazeDrawer().draw(maze), sep="\n")
