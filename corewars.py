import argparse
import sys

from src.file import get_warrior_list
from src.game import Game
from src.gui.gui import PyGameGUI

SCREEN_X = 1200
SCREEN_Y = 800


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('warriors', nargs='*')
    parser.add_argument('--core-size', nargs='?', default=8000)
    return parser.parse_args(args[1:])


def main(args):
    args = parse_args(args)
    warriors = get_warrior_list(args.warriors)
    core_size = int(args.core_size)
    # Init gui
    gui = PyGameGUI(SCREEN_X, SCREEN_Y, core_size)
    # Init game
    game = Game(warriors, core_size, gui, 10)
    # Play game
    game.play()
    # Close gui
    gui.close()


if __name__ == '__main__':
    main(sys.argv)
