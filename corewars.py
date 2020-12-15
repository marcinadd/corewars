from io import StringIO

from src.game import Game
from src.parser import *


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
    # Init game
    game = Game([warrior], core_size=200)
    # Simulate
    while True:
        # TODO Check if there is any alive warrior process
        game.simulation_step()


if __name__ == '__main__':
    main()
