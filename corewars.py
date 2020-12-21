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
    parser.add_argument('warrior_files', nargs='*')
    return parser.parse_args(args[1:])


def main(args):
    args = parse_args(args)
    warriors = get_warrior_list(args.warrior_files)
    # Init gui
    gui = PyGameGUI(SCREEN_X, SCREEN_Y)
    # Init game
    game = Game(warriors, core_size=8000, gui=gui)

    # Simulate
    while game.has_alive_warriors():
        game.simulation_step()
        gui.clock_tick()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main(sys.argv)
