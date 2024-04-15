from argparse import Namespace

from src.Maze import MazeConfig
from src.MazeFileManager import MazeFileManager
from src.actions.Action import Action
from src.drawers.TextMazeDrawer import TextMazeDrawer, TextMazeDrawMode
from src.generators.DFSGenerator import DFSGenerator
from src.generators.SpanningTreeGenerator import SpanningTreeGenerator


class GenerateAction(Action):
    name = "generate"
    help = "Generate maze and store it into file."

    generators = {
        "dfs": DFSGenerator(),
        "tree": SpanningTreeGenerator()
    }

    @staticmethod
    def add_subparser(parser):
        subparser = parser.add_parser(GenerateAction.name, help=GenerateAction.help)
        subparser.add_argument("-f", dest="path", type=str, help='File path to store maze to.', required=False)
        subparser.add_argument("-p", dest="print", action="store_true", help='Should maze be printed.', required=False)

        subparser.add_argument("-W", "--width", dest="width", type=int, help='Maze width.', required=False, default=5)
        subparser.add_argument("-H", "--height", dest="height", type=int, help='Maze height.', required=False,
                               default=5)

        generators = list(GenerateAction.generators.keys())
        subparser.add_argument("-g", dest="generator", choices=generators, help='Method for maze generation.',
                               required=False, default=generators[0])

    @staticmethod
    def handle(args: Namespace):
        maze_config = MazeConfig(args.width, args.height)

        chosen_generator = GenerateAction.generators[args.generator]
        maze = chosen_generator.generate(maze_config)

        if args.print:
            print(*TextMazeDrawer().draw(maze), sep="\n")

        if args.path is not None:
            MazeFileManager.write_into_file(args.path, maze)
