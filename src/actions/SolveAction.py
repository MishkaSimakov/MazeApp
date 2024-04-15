from argparse import Namespace

from src.MazeFileManager import MazeFileManager
from src.actions.Action import Action
from src.drawers.TextMazeDrawer import TextMazeDrawer, TextThickMazeDrawer
from src.solvers.BFSMazeSolver import BFSMazeSolver


class SolveAction(Action):
    name = "solve"
    help = "Solve maze."

    @staticmethod
    def add_subparser(parser):
        subparser = parser.add_parser(SolveAction.name, help=SolveAction.help)
        subparser.add_argument('-f', dest="path", required=True, type=str, help='File to read maze from.')

    @staticmethod
    def handle(args: Namespace):
        maze = MazeFileManager.read_from_file(args.path)

        if not maze:
            print("Error occurred while reading file.")
            return

        solution = BFSMazeSolver.solve(maze)
        print(*TextMazeDrawer().draw(maze, solution), sep="\n")
