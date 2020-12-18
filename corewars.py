from io import StringIO

import pygame

from src.game import Game
from src.gui.gui import PyGameGUI
from src.parser import *

SCREEN_X = 1024
SCREEN_Y = 768


def main():
    # TODO Read from file
    data = """
        ADD.AB #4, 3
        MOV.I  2, @2
        JMP    -2 ; Useless comment for parsing test
        DAT    #0, #0
        """
    file_handle = StringIO(data)
    # Parse warrior
    warrior = parse_warrior(file_handle)
    # Init gui
    gui = PyGameGUI(SCREEN_X, SCREEN_Y)
    # Init game
    game = Game([warrior], core_size=8000, gui=gui)

    # Simulate
    while game.has_alive_warriors():
        game.simulation_step()
        gui.clock_tick()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
