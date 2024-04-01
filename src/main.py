import argparse
from src.actions.GenerateAction import GenerateAction
from src.actions.PrintAction import PrintAction
from src.actions.SolveAction import SolveAction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Maze Generator',
        description='This program generates and manages mazes.'
    )

    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True

    actions = [GenerateAction, PrintAction, SolveAction]

    for action in actions:
        action.add_subparser(subparsers)

    args = parser.parse_args()

    for action in actions:
        if action.name == args.action:
            action.handle(args)
            break
