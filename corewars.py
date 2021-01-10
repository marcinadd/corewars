#!/usr/bin/env python3
import argparse
import sys

from src.args import IntBetween, check_warrior_count
from src.config import SCREEN_X, SCREEN_Y
from src.file import get_warrior_list
from src.game import Game
from src.gui.gui import PyGameGUI, MockGUI


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('warriors', nargs='*', action=check_warrior_count(5))
    parser.add_argument('--rounds', nargs='?', default=10, type=IntBetween(1, 10))
    parser.add_argument('--core-size', nargs='?', default=8000, type=IntBetween(100, 8000))
    parser.add_argument('--max-cycles', nargs='?', default=80000, type=IntBetween(100, 100000))
    parser.add_argument('--no-gui', action='store_true')
    return parser.parse_args(args[1:])


def main(args):
    args = parse_args(args)
    warriors = get_warrior_list(args.warriors)
    # Get args
    core_size = int(args.core_size)
    rounds = int(args.rounds)
    max_cycles = int(args.max_cycles)
    no_gui = args.no_gui
    # Init gui
    if no_gui:
        gui = MockGUI(core_size)
    else:
        gui = PyGameGUI(SCREEN_X, SCREEN_Y, core_size)
    # Init game
    game = Game(warriors, core_size, gui, rounds, max_cycles)
    # Play game
    game.play()
    # Print results
    print(game.get_results_string())
    # Close gui
    gui.close()


if __name__ == '__main__':
    main(sys.argv)
