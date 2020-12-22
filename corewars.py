import argparse
import sys

import pygame

from src.file import get_warrior_list
from src.game import Game
from src.gui.gui import PyGameGUI

SCREEN_X = 1024
SCREEN_Y = 768


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
    game = Game(warriors, core_size=core_size, gui=gui)

    # Simulate
    while game.has_alive_warriors():
        game.simulation_step()
        gui.clock_tick()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main(sys.argv)
