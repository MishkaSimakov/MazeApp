from argparse import Namespace

from src.Maze import MazeConfig
from src.MazeFileManager import MazeFileManager
from src.actions.Action import Action
from src.drawers.TextMazeDrawer import TextMazeDrawer, TextMazeDrawMode
from src.generators.DFSGenerator import DFSGenerator


class GenerateAction(Action):
    name = "generate"
    help = "Generate maze and store it into file."

    @staticmethod
    def add_subparser(parser):
        subparser = parser.add_parser(GenerateAction.name, help=GenerateAction.help)
        subparser.add_argument("-f", dest="path", type=str, help='File path to store maze to.', required=False)
        subparser.add_argument("-p", dest="print", action="store_true", help='Should maze be printed.', required=False)
        # TODO: fix height
        subparser.add_argument("--width", dest="width", type=int, help='Maze width.', required=False, default=20)
        subparser.add_argument("--height", dest="height", type=int, help='Maze height.', required=False, default=20)

    @staticmethod
    def handle(args: Namespace):
        maze_config = MazeConfig(args.width, args.height)
        maze = DFSGenerator().generate(maze_config)

        if args.print:
            print(*TextMazeDrawer(draw_mode=TextMazeDrawMode.THIN).draw(maze), sep="\n")

        if args.path is not None:
            MazeFileManager.write_into_file(args.path, maze)
