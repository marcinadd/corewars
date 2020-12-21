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
MOV.i	$0,	$-396
SEQ.i	}-1,	$5
JMP.b	$-2,	>-2

SPL.b	$-399,	#0

spl.b	#2,	}0
mov.i	$2,	}-1
dat.f	}-2,	}-2
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
